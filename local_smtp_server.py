#!/usr/bin/env python3
import asyncio
import sys

class LocalSMTPServer:
    def __init__(self, host="127.0.0.1", port=1025):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        print(f"\n[server] Connection accepted from {writer.get_extra_info('peername')}")
        writer.write(b"220 Local SMTP Debugging Server Ready\r\n")
        await writer.drain()

        in_data = False
        data_buffer = []

        try:
            while True:
                line_bytes = await reader.readline()
                if not line_bytes:
                    break

                try:
                    line = line_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    line = line_bytes.decode("latin-1")

                stripped = line.strip()

                if in_data:
                    if stripped == ".":
                        in_data = False
                        raw_email = "".join(data_buffer)
                        print("\n" + "="*50)
                        print("RECEIVED EMAIL CONTENTS:")
                        print("="*50)
                        print(raw_email)
                        print("="*50 + "\n")
                        data_buffer = []
                        writer.write(b"250 OK Message accepted\r\n")
                        await writer.drain()
                    else:
                        # Handle dot stuffing (if line starts with a dot, strip the leading dot)
                        if line.startswith("."):
                            line = line[1:]
                        data_buffer.append(line)
                    continue

                upper = stripped.upper()
                if upper.startswith(("EHLO", "HELO")):
                    # Advertise AUTH support so smtplib.login() works
                    writer.write(b"250-localhost\r\n250 AUTH PLAIN LOGIN\r\n")
                elif upper.startswith("AUTH"):
                    writer.write(b"235 2.7.0 Authentication successful\r\n")
                elif upper.startswith("MAIL FROM:"):
                    writer.write(b"250 2.1.0 OK\r\n")
                elif upper.startswith("RCPT TO:"):
                    writer.write(b"250 2.1.5 OK\r\n")
                elif upper == "DATA":
                    in_data = True
                    writer.write(b"354 Start mail input; end with <CR><LF>.<CR><LF>\r\n")
                elif upper == "QUIT":
                    writer.write(b"221 2.0.0 Bye\r\n")
                    await writer.drain()
                    break
                elif upper == "NOOP":
                    writer.write(b"250 OK\r\n")
                elif upper == "RSET":
                    data_buffer = []
                    in_data = False
                    writer.write(b"250 OK\r\n")
                else:
                    writer.write(b"500 5.5.1 Command unrecognized\r\n")

                await writer.drain()
        except Exception as e:
            print(f"[server] Error handling connection: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print("[server] Connection closed.")

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"[server] Local SMTP Test Server running on smtp://{addr[0]}:{addr[1]}")
        print("Keep this server running to receive emails.")
        print("Press Ctrl+C to stop.")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = LocalSMTPServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nStopping Local SMTP Server...")
