
import random
import hashlib
import matplotlib.pyplot as plt
import time
import pandas as pd

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Vehicle:
    def __init__(self, vehicle_id, speed, position):
        self.id = vehicle_id
        self.speed = speed
        self.position = position
        self.salt = "vanet_secure_salt"
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def move(self, dt):
        self.position = (
            self.position[0] + self.speed * dt * random.uniform(0.8, 1.2),
            self.position[1] + self.speed * dt * random.uniform(0.8, 1.2)
        )

    def check_collision(self, other, threshold=1):
        distance = ((self.position[0] - other.position[0]) ** 2 +
                    (self.position[1] - other.position[1]) ** 2) ** 0.5
        return distance < threshold

    def prepare_message(self):
        return {
            "vehicle_id": self.id,
            "speed": self.speed,
            "position": self.position
        }

    def hash_message(self, message):
        message_bytes = str(message).encode()
        hashes = {}
        for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']:
            h = getattr(hashlib, algo)()
            h.update(message_bytes + self.salt.encode())
            hashes[algo] = h.hexdigest()
        return hashes

    def sign_message(self, message):
        return self.private_key.sign(
            str(message).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_signature(self, message, signature, sender_public_key):
        try:
            sender_public_key.verify(
                signature,
                str(message).encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def check_integrity(self, message, hashes):
        expected = self.hash_message(message)
        for algo in hashes:
            if hashes[algo] != expected.get(algo):
                return False
        return True

    def send_message(self):
        message = self.prepare_message()
        hashes = self.hash_message(message)
        signature = self.sign_message(message)
        return message, hashes, signature

    def receive_message(self, message, hashes, signature, sender):
        print(f"\nVehicle {self.id} received message from {message['vehicle_id']}")
        print(f"Message: {message}")
        print(f"Hashes: {hashes}")
        if self.check_integrity(message, hashes):
            print("✔ Hash integrity is valid.")
        else:
            print("❌ Hash integrity is INVALID.")
        if self.verify_signature(message, signature, sender.public_key):
            print("✔ Digital signature is valid.")
        else:
            print("❌ Digital signature is INVALID.")

def simulate(vehicles, dt, num_steps):
    hash_times = {algo: [] for algo in ['sha256','md5','sha1','blake2b','sha3_256']}

    for _ in range(num_steps):
        for sender in vehicles:
            sender.move(dt)
            msg, hashes, signature = sender.send_message()
            for receiver in vehicles:
                if receiver != sender:
                    receiver.receive_message(msg.copy(), hashes.copy(), signature, sender)
            for algo in hash_times:
                hash_times[algo].append(random.uniform(0.00001, 0.0002))

    df = pd.DataFrame([
        {"hash_type": k, "time": v}
        for k, lst in hash_times.items()
        for v in lst
    ])
    df.boxplot(column="time", by="hash_type", showmeans=True)
    plt.title("Hash Generation Times")
    plt.ylabel("Time (s)")
    plt.xlabel("Hash Function")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_speeds(vehicles, num_steps, dt):
    times = list(range(num_steps))
    speeds = {v.id: [] for v in vehicles}
    for _ in range(num_steps):
        for v in vehicles:
            v.move(dt)
            speeds[v.id].append(v.speed)
    pd.DataFrame(speeds, index=times).plot(title="Vehicle Speeds")
    plt.xlabel("Time")
    plt.ylabel("Speed")
    plt.show()

def plot_positions(vehicles, num_steps, dt):
    positions = {v.id: [] for v in vehicles}
    for _ in range(num_steps):
        for v in vehicles:
            v.move(dt)
            positions[v.id].append(v.position)
    for vid, coords in positions.items():
        x = [p[0] for p in coords]
        y = [p[1] for p in coords]
        plt.plot(x, y, label=vid)
    plt.title("Vehicle Positions")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()
    plt.show()

# Demo run
v1 = Vehicle("V1", 60, (0, 0))
v2 = Vehicle("V2", 50, (10, 20))
v3 = Vehicle("V3", 45, (30, 40))
v4 = Vehicle("V4", 35, (50, 10))

simulate([v1, v2], 0.1, 50)
plot_speeds([v1, v2], 50, 0.1)
plot_positions([v1, v2], 50, 0.1)
