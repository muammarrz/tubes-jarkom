import socket

HOST = 'localhost'
PORT = 8000

def run_server():
    
    # Implementasi pembuatan TCP socket dan mengaitkannya ke alamat dan port tertentu 
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # membuat socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # membolehkan server socket untuk menggunakan kembali address dan port
        server_socket.bind((HOST, PORT)) # mengaitkan socket ke port
        server_socket.listen() # mendengarkan permintaan koneksi TCP dari klien.

        print(f'Mendengarkan permintaan pada port {PORT}...')

        while True:
            client_socket, client_address = server_socket.accept() #membuat socket untuk client dan membuat koneksi
            print(f'Client {client_address} telah terhubung ke server.')
            handle_request(client_socket) # menjalankan fungsi handle request
            client_socket.close() # menutup koneksi socket client
            
def handle_request(client_socket):

    #Program web server menerima dan memparsing HTTP request yang dikirimkan oleh browser
    
    request_data = client_socket.recv(1024).decode() # menerima data dari client socket dan didecode dari bytes ke string
    if not request_data: #jika tidak ada request memberhentikan fungsi
        return
 
    method, file_name, _ = request_data.split(' ', 2) # parsing http request
    
    # Web server mencari dan mengambil file (dari file system) yang diminta oleh client
    try:
        if file_name != '/':
            f = open(file_name[1:]) #membuka file di local directory
            file_content = f.read() #membaca data
    except:
        file_name = 'ERROR' #error handling jika tidak ada file yg dicari
    
    if method == 'GET' and file_name != 'ERROR': # jika client merequest file
        
        #Web server membuat HTTP response message yang terdiri dari header dan konten file yang diminta
        if file_name == '/':
            response_body = '<html><head><title>Welcome to my webserver</title></head><body><h1>Welcome to my webserver</h1></body></html>' #respon jika client tidak meminta file apapun
        else:
            response_body = file_content #respon konten file yang diminta jika ada
        response_headers = [ #respon header
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            f'Content-Length: {len(response_body)}',
            'Connection: close',
        ]
        response = '\r\n'.join(response_headers) + '\r\n\r\n' + response_body # gabungkan header dan body
    else:
        # jika file yang diminta oleh client tidak tersedia, web server mengirimkan pesan “404 Not Found” dan dapat ditampilkan dengan benar di sisi client.
        
        response_body = '<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>' #respon jika file yang dicari tidak ditemukan
        response_headers = [
            'HTTP/1.1 404 Not Found',
            'Content-Type: text/html',
            f'Content-Length: {len(response_body)}',
            'Connection: close',
        ]
        response = '\r\n'.join(response_headers) + '\r\n\r\n' + response_body

    #Web server mengirimkan response message yang sudah dibuat ke browser (client) dan dapat ditampilkan dengan benar di sisi client.
    client_socket.sendall(response.encode())



if __name__ == '__main__': #buat jalanin
    run_server()
