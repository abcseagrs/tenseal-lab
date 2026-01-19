# pc_b.py
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

def run_pc_b():
    # docker-compose 사용 시: 'pc_a'
    # 실제 2PC 실습 시: 상대방 IP 입력
    host_ip = input("PC A의 IP 주소 (docker-compose면 'pc_a' 입력): ")
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[B] {host_ip}:{port} 에 연결 시도 중...")
        client_socket.connect((host_ip, port))
        print("[B] 연결 성공!")

        # 1. A로부터 Public Context 수신
        context_proto = recv_data(client_socket)
        context = ts.context_from(context_proto)
        print("[B] Public Context 수신 완료")

        # 2. 나의 데이터 암호화
        my_data = [30, 40]
        enc_b = ts.bfv_vector(context, my_data)
        print(f"[B] 내 데이터: {my_data} → 암호화 완료")

        # 3. 암호화 데이터를 A에게 전송
        send_data(client_socket, enc_b.serialize())
        print("[B] 암호화 데이터 전송 완료")

        print("=" * 40)
        print("[B] 전송 완료! 결과는 PC A에서 확인하세요.")
        print("=" * 40)

    except ConnectionRefusedError:
        print("[B] 연결 실패: PC A가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"[B] 오류 발생: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    run_pc_b()
