"""Upload the HatLights MicroPython runtime over a serial REPL connection."""

import argparse
import base64
from pathlib import Path

import serial


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEVICE_ROOT = PROJECT_ROOT / "device"
EXCLUDED_FILENAMES = {"secrets.example.py"}
ENCODED_CHUNK_SIZE = 384


def device_files():
    files = []
    for source_path in DEVICE_ROOT.rglob("*.py"):
        if "__pycache__" in source_path.parts:
            continue
        if source_path.name in EXCLUDED_FILENAMES:
            continue
        files.append(source_path)
    return sorted(files, key=lambda path: path.relative_to(DEVICE_ROOT).as_posix())


class RawReplUploader:
    def __init__(self, port):
        self.board = serial.Serial(port, 115200, timeout=3, write_timeout=3)

    def close(self):
        self.board.close()

    def enter_raw_repl(self):
        self.board.write(b"\x02\r\x03\x03")
        self.board.read(256)
        self.board.reset_input_buffer()
        self.board.write(b"\x01")
        banner = self.board.read(256)
        if b"raw REPL" not in banner:
            raise RuntimeError("Could not enter raw REPL: {!r}".format(banner))
        self.board.reset_input_buffer()

    def run(self, source):
        self.board.write(source.encode("utf-8") + b"\x04")
        stdout = self.board.read_until(b"\x04")
        stderr = self.board.read_until(b"\x04")
        if b"OK" not in stdout or stderr.strip(b"\x04\r\n"):
            raise RuntimeError(
                "Board rejected command. stdout={!r}, stderr={!r}".format(stdout, stderr)
            )

    def upload_file(self, source_path):
        board_path = source_path.relative_to(DEVICE_ROOT).as_posix()
        parent = Path(board_path).parent.as_posix()
        if parent != ".":
            self.run(
                "import os; ({!r} in os.listdir()) or os.mkdir({!r})".format(
                    parent, parent
                )
            )

        compiled_path = Path(board_path).with_suffix(".mpy").as_posix()
        compiled_parent = Path(compiled_path).parent.as_posix()
        self.run(
            "import os; ({!r} in os.listdir({!r})) and os.remove({!r})".format(
                Path(compiled_path).name, compiled_parent, compiled_path
            )
        )
        self.run("import ubinascii; file_handle=open({!r}, 'wb')".format(board_path))
        encoded = base64.b64encode(source_path.read_bytes())
        for offset in range(0, len(encoded), ENCODED_CHUNK_SIZE):
            chunk = encoded[offset : offset + ENCODED_CHUNK_SIZE]
            self.run("file_handle.write(ubinascii.a2b_base64({!r}))".format(chunk))
        self.run("file_handle.close()")
        print("Uploaded {}".format(board_path))

    def soft_reset(self):
        self.board.write(b"\x02")
        self.board.read(256)
        self.board.write(b"\x04")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM5", help="Board serial port (default: COM5)")
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Leave the board at the REPL instead of soft-resetting after upload",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    files = device_files()
    if not files:
        raise RuntimeError("No device files found in {}".format(DEVICE_ROOT))

    uploader = RawReplUploader(args.port)
    try:
        uploader.enter_raw_repl()
        for source_path in files:
            uploader.upload_file(source_path)
        if not args.no_reset:
            uploader.soft_reset()
    finally:
        uploader.close()

    print("Uploaded {} files to {}.".format(len(files), args.port))


if __name__ == "__main__":
    main()