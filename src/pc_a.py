# pc_a.py
import tenseal as ts
import socket
import struct


# === 유틸리티 함수 ===

def send_data(sock, data: bytes):
    """데이터 길이를 먼저 보내고, 이어서 데이터 전송"""
    length = len(data)
    sock.sendall(struct.pack('>I', length))
    sock.sendall(data)


def recv_data(sock) -> bytes:
    """데이터 길이를 먼저 받고, 해당 길이만큼 수신"""
    raw_length = recv_exact(sock, 4)
    length = struct.unpack('>I', raw_length)[0]
    return recv_exact(sock, length)


def recv_exact(sock, n: int) -> bytes:
    """정확히 n바이트를 수신할 때까지 반복"""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("연결이 끊어졌습니다")
        data += packet
    return data


# === 메인 로직 ===

def run_pc_a():
    # 1. 동형암호 컨텍스트 및 키 생성
    print("[A] 동형암호 키 생성 중...")
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=4096,
        plain_modulus=1032193
    )
    context.generate_relin_keys()
    secret_key = context.secret_key()  # 비밀키 보관 (복호화용)

    # 2. 나의 데이터 암호화
    my_data = [10, 20]
    enc_a = ts.bfv_vector(context, my_data)
    print(f"[A] 내 데이터: {my_data}")

    # 3. 서버 소켓 설정
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)

    print("[A] PC B의 접속 대기 중... (Port: 5000)")

    conn, addr = server_socket.accept()
    print(f"[A] PC B 접속 완료: {addr}")

    try:
        # 4. Public Context 전송 (비밀키 제외)
        public_context = context.copy()
        public_context.make_context_public()
        send_data(conn, public_context.serialize())
        print("[A] Public Context 전송 완료")

        # 5. B의 암호화 데이터 수신
        data_b_proto = recv_data(conn)
        enc_b = ts.lazy_bfv_vector_from(data_b_proto)
        enc_b.link_context(context)
        print("[A] B의 암호화 데이터 수신 완료")

        # 6. 암호화 상태에서 덧셈 → 복호화
        result_enc = enc_a + enc_b
        final_result = result_enc.decrypt(secret_key)

        print("=" * 40)
        print(f"[결과] A의 데이터: {my_data}")
        print(f"[결과] 합산 (복호화): {final_result}")
        print("=" * 40)

    except Exception as e:
        print(f"[A] 오류 발생: {e}")

    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    run_pc_a()
