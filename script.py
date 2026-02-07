import requests, uuid, random, re, json, urllib.parse, base64, os, string, time
from datetime import datetime


# -----------------------------------------------------------------------------
# GLOBAL REQUEST DELAY & NETWORK MONITOR (Monkey Patching)
# -----------------------------------------------------------------------------
# 1. Random Delay: Mimics human behavior.
# 2. Network Monitor: Logs suspicious responses (blocks, challenges) to analyze
#    why Instagram might be "swearing" at us.
# -----------------------------------------------------------------------------
original_get = requests.get
original_post = requests.post

def random_sleep(min_time=1.0, max_time=3.0):
    """Sleep for a random amount of time to mimic human behavior."""
    sleep_time = random.uniform(min_time, max_time)
    time.sleep(sleep_time)

def log_transaction(method, url, response, payload=None):
    """Logs suspicious network packets to a file for analysis."""
    try:
        # Filter: Only log if status is NOT 200 OR if response contains "challenge" / "feedback"
        is_suspicious = (response.status_code != 200) or \
                        ("challenge" in response.text) or \
                        ("feedback_required" in response.text) or \
                        ("wait" in response.text)

        if is_suspicious:
            with open("network_monitor.log", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n{'='*60}\n")
                f.write(f"TIME: {timestamp}\n")
                f.write(f"REQUEST: [{method}] {url}\n")
                if payload:
                    # simplistic redaction of password if present
                    safe_payload = str(payload)
                    if "password" in safe_payload:
                        safe_payload = safe_payload.replace(payload.get('password', ''), '***')
                    f.write(f"PAYLOAD: {safe_payload}\n")
                
                f.write(f"RESPONSE CODE: {response.status_code}\n")
                f.write(f"HEADERS: {dict(response.headers)}\n")
                f.write(f"BODY (First 1000 chars):\n{response.text[:1000]}\n")
                f.write(f"{'='*60}\n")
            
            # Optional: Alert user in console
            print(f"\n[!] NETWORK ALERT: Suspicious response detected! ({response.status_code})")
            print(f"    Check 'network_monitor.log' for details.\n")

    except Exception as e:
        print(f"Logging failed: {e}")

def patched_get(*args, **kwargs):
    """Wrapper for requests.get with random delay and logging."""
    random_sleep(0.8, 1.8)
    response = original_get(*args, **kwargs)
    
    # Log the packet if needed
    url = args[0] if len(args) > 0 else kwargs.get('url', 'Unknown URL')
    log_transaction("GET", url, response)
    
    return response

def patched_post(*args, **kwargs):
    """Wrapper for requests.post with random delay and logging."""
    random_sleep(1.5, 3.5)
    response = original_post(*args, **kwargs)
    
    # Log the packet if needed
    url = args[0] if len(args) > 0 else kwargs.get('url', 'Unknown URL')
    data = kwargs.get('data', None)
    log_transaction("POST", url, response, payload=data)
    
    return response

# Apply patches
requests.get = patched_get
requests.post = patched_post
# -----------------------------------------------------------------------------


class InstagramNameChanger:
    def __init__(self, session_id, user_id=None):
        """
        Initialize the tool with session_id
        
        Args:
            session_id (str): Instagram sessionid
            user_id (str): Instagram user ID (optional, will extract from session)
        """
        self.session_id = session_id
        
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = self.extract_user_id_from_session()
        
        
        self.device_id = f"android-{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:12]}"
        self.android_id = f"android-{uuid.uuid4().hex[:16]}"
        self.family_device_id = f"{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:12]}"
        self.app_id = "567067343352427"
        
        
        self.mid = "aUuvHgABAAEyNNrqgv4MT_Kbuoku"
        self.pigeon_session_id = f"UFS-{uuid.uuid4()}-0"
        
        
        self.bloks_version_id = "5f56efad68e1" # Update for v365
        self.ig_capabilities = "3brTv10="
        self.ig_www_claim = "hmac.AR1AT8scPp6CMKFZBaO9CjDMY6Y6rqfmbDZkDIJvZ7jZXaUO"
        
        
        self.auth_token = None
        self.last_token_refresh = 0
        
        
        self.salt_ids = "332021310,332016293,332010360,332011758"
        self.salt_logger_ids = "915219134,76228318,936453575,76226099,915222997,915222759,883764695,76221888,25952257,42991646,750984636,915216738"
        
        
        self.user_agent = self.generate_user_agent()
    
    def extract_user_id_from_session(self):
        """
        Extract user_id from session_id
        
        Returns:
            str: User ID
        """
        try:
            if "%3A" in self.session_id:
                return self.session_id.split("%3A")[0]
            elif ":" in self.session_id:
                return self.session_id.split(":")[0]
            else:
                return ""
        except:
            return ""
    
    def make_token(self):
        """
        Convert sessionid to authorization token
        
        Returns:
            str: Base64 encoded authorization token
        """
        try:
            ds_user_id = self.user_id
            auth_payload = f'{{"ds_user_id":"{ds_user_id}","sessionid":"{self.session_id}"}}'
            
            encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')
            return encoded_auth
            
        except Exception as e:
            print(f"[!] Error creating token: {e}")
            return None
    
    def generate_user_agent(self):
        android_versions = ["30/11", "31/12", "33/13", "34/14"]
        dpi_options = ["420dpi", "480dpi", "560dpi", "640dpi"]
        resolution_options = ["1080x1920", "1440x2560", "1080x2400", "1440x3200"]
        devices = ["samsung", "xiaomi", "google", "oneplus", "oppo"]
        models = ["SM-S908B", "2201123G", "Pixel 7 Pro", "LE2123", "CPH2357"]
        
        version = random.choice(android_versions)
        dpi = random.choice(dpi_options)
        resolution = random.choice(resolution_options)
        device = random.choice(devices)
        model = random.choice(models)
        code = random.randint(100000000, 999999999)
        
        return f"Instagram 365.0.0.14.102 Android ({version}; {dpi}; {resolution}; {device}; {model}; {model}; qcom; en_US; {code})"
    
    def get_nav_chain(self):
        """
        Generate dynamic navigation chain
        
        Returns:
            str: Updated navigation chain
        """
        timestamp = int(time.time() * 1000)
        random_ms = random.randint(100, 999)
        
        nav_chain = (
            f"SelfFragment:self_profile:2:main_profile:{timestamp}.{random_ms}:::1768075571.3,"
            f"ProfileMediaTabFragment:self_profile:3:button:{timestamp}.{random_ms+100}:::1768075572.263,"
            f"EditProfileFragment:edit_profile:4:button:{timestamp}.{random_ms+200}:::1768075583.680,"
            f"EditFullNameFragment:profile_edit_full_name:5:button:{timestamp}.{random_ms+300}:::1768075586.166"
        )
        
        return nav_chain
    
    def get_current_name(self):
        """
        Get current profile name
        
        Returns:
            dict: Result with current name or error
        """
        try:
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": f"sessionid={self.session_id}",
                "ig-u-ds-user-id": self.user_id
            }
            
            response = requests.get(
                "https://i.instagram.com/api/v1/accounts/current_user/?edit=true",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                current_name = data.get("user", {}).get("full_name", "")
                return {"success": True, "current_name": current_name}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_profile_name(self, new_name=""):
        """
        Change Instagram account name
        
        Args:
            new_name (str): New name (empty to remove name)
        
        Returns:
            dict: Operation result
        """
        try:
            
            data = f"first_name={urllib.parse.quote(new_name)}&_uuid={self.device_id}"
            
            
            headers = {
                "Host": "i.instagram.com",
                "X-Ig-App-Locale": "en_US",
                "X-Ig-Device-Locale": "en_US",
                "X-Ig-Mapped-Locale": "en_US",
                "X-Pigeon-Session-Id": self.pigeon_session_id,
                "X-Pigeon-Rawclienttime": str(time.time()),
                "X-Ig-Bandwidth-Speed-Kbps": "1005.000",
                "X-Ig-Bandwidth-Totalbytes-B": "4522018",
                "X-Ig-Bandwidth-Totaltime-Ms": "3990",
                "X-Bloks-Version-Id": self.bloks_version_id,
                "X-Ig-Www-Claim": self.ig_www_claim,
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "X-Bloks-Prism-Colors-Enabled": "true",
                "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
                "X-Bloks-Prism-Font-Enabled": "false",
                "X-Bloks-Is-Layout-Rtl": "false",
                "X-Ig-Device-Id": self.device_id,
                "X-Ig-Family-Device-Id": self.family_device_id,
                "X-Ig-Android-Id": self.android_id,
                "X-Ig-Timezone-Offset": "28800",
                "X-Ig-Nav-Chain": self.get_nav_chain(),
                "X-Ig-Salt-Ids": self.salt_ids,
                "X-Fb-Connection-Type": "WIFI",
                "X-Ig-Connection-Type": "WIFI",
                "X-Fb-Network-Properties": "Validated;LocalAddrs=/fe80::8efd:f0ff:fef1:b294,/192.168.232.2,;",
                "X-Ig-Capabilities": self.ig_capabilities,
                "X-Ig-App-Id": self.app_id,
                "User-Agent": self.user_agent,
                "Accept-Language": "en-US",
                "Cookie": f"sessionid={self.session_id}; ds_user_id={self.user_id}",
                "X-Mid": self.mid,
                "Ig-U-Ds-User-Id": self.user_id,
                "Ig-U-Rur": f"LDC,{self.user_id},1799611591:01feff23e2cc023107e8e817be29a3fd62251fc21009256c6cf4a394311f5eeb1032dec9",
                "Ig-Intended-User-Id": self.user_id,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept-Encoding": "gzip, deflate",
                "X-Fb-Http-Engine": "Liger",
                "X-Fb-Client-Ip": "True",
                "X-Fb-Server-Cluster": "True"
            }
            
            
            url = "https://i.instagram.com/api/v1/accounts/update_profile_name/"
            
            action = f"Setting name to: '{new_name}'" if new_name else "Removing current name"
            print(f"   {action}")
            
            response = requests.post(url, headers=headers, data=data, timeout=15)
            
            
            result = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "action": "SET" if new_name else "REMOVE",
                "new_name": new_name
            }
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    result["json_response"] = json_response
                    
                    if json_response.get("status") == "ok":
                        result["message"] = "   [+] Name updated successfully!" if new_name else "   [+] Name removed successfully!"
                    else:
                        result["error"] = f"Instagram rejected request: {json_response}"
                except json.JSONDecodeError:
                    result["error"] = "Invalid response from Instagram"
            else:
                result["error"] = f"Request failed with status: {response.status_code}"
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {e}"
            return {
                "success": False,
                "error": error_msg,
                "status_code": None
            }
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            return {
                "success": False,
                "error": error_msg,
                "status_code": None
            }
    
    def batch_update_names(self, names_list, delay_seconds=5):
        """
        Change names sequentially (to avoid blocks)
        
        Args:
            names_list (list): List of names to set
            delay_seconds (int): Delay between changes
        
        Returns:
            list: Results of all attempts
        """
        results = []
        
        print(f"   Starting to change {len(names_list)} names...")
        
        for i, name in enumerate(names_list, 1):
            print(f"\n   [{i}/{len(names_list)}] Processing name: '{name}'")
            
            result = self.update_profile_name(name)
            results.append(result)
            
            if result.get("success"):
                print(f"   [+] Success!")
            else:
                print(f"   [!] Failed: {result.get('error', 'Unknown error')}")
            
            
            if i < len(names_list) and delay_seconds > 0:
                print(f"   [⏳] Waiting {delay_seconds} seconds before next...")
                time.sleep(delay_seconds)
        
        
        success_count = sum(1 for r in results if r.get("success"))
        print(f"\n   {'='*40}")
        print(f"   Results Summary:")
        print(f"      Successful: {success_count}")
        print(f"      Failed: {len(results) - success_count}")
        print(f"      Total: {len(results)}")
        print(f"   {'='*40}")
        
        return results


def get_session_code():
    print("="*60)
    print("GET SESSION (CODE)")
    print("="*60)
    
    timestamp = str(int(time.time()))

    def RandomString(n=10):
        letters = string.ascii_lowercase + '1234567890'
        return ''.join(random.choice(letters) for i in range(n))

    def RandomStringUpper(n=10):
        letters = string.ascii_uppercase + '1234567890'
        return ''.join(random.choice(letters) for i in range(n))

    def RandomStringChars(n=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(n))

    def randomStringWithChar(stringLength=10):
        letters = string.ascii_lowercase + '1234567890'
        result = ''.join(random.choice(letters) for i in range(stringLength - 1))
        return RandomStringChars(1) + result

    uu = '83f2000a-4b95-4811-bc8d-0f3539ef07cf'

    class sessting:
        def __init__(self):
            pass
        
        def generateUSER_AGENT(self):
            android_versions = ["30/11", "31/12", "33/13", "34/14"]
            dpi_options = ["420dpi", "480dpi", "560dpi", "640dpi"]
            resolution_options = ["1080x1920", "1440x2560", "1080x2400", "1440x3200"]
            devices = ["samsung", "xiaomi", "google", "oneplus", "oppo"]
            models = ["SM-S908B", "2201123G", "Pixel 7 Pro", "LE2123", "CPH2357"]
            
            version = random.choice(android_versions)
            dpi = random.choice(dpi_options)
            resolution = random.choice(resolution_options)
            device = random.choice(devices)
            model = random.choice(models)
            code = random.randint(100000000, 999999999)
            
            return f"Instagram 365.0.0.14.102 Android ({version}; {dpi}; {resolution}; {device}; {model}; {model}; qcom; en_US; {code})"
        
        def generate_DeviceId(self, ID):
            import hashlib
            volatile_ID = "12345"
            m = hashlib.md5()
            m.update(ID.encode('utf-8') + volatile_ID.encode('utf-8'))
            return 'android-' + m.hexdigest()[:16]
        
    class login:
        def __init__(self):
            self.sesstings = sessting()
            self.coo = None
            self.token = None
            self.mid = None
            self.sessionid = None
            self.Login()
        
        def headers_login(self):
            headers = {}
            headers['User-Agent'] = self.sesstings.generateUSER_AGENT()
            headers['Host'] = 'i.instagram.com'
            headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['accept-encoding'] = 'gzip, deflate'
            headers['x-fb-http-engine'] = 'Liger'
            headers['Connection'] = 'close'
            return headers
        
        def checkpoint(self):
            info = requests.get(f"https://i.instagram.com/api/v1{self.req.json()['challenge']['api_path']}", headers=self.headers_login(), cookies=self.coo)
            step_data = info.json()["step_data"]
            if "phone_number" in step_data:
                try:
                    phone = info.json()["step_data"]["phone_number"]
                    print(f'[0] phone_number : {phone}')
                except:
                    pass
            elif "email" in step_data:
                try:
                    email = info.json()["step_data"]["email"]
                    print(f'[1] email : {email}')
                except:
                    pass

            else:
                print("unknown verification method")
                input()
                exit()
            return self.send_choice()
        
        def send_choice(self):
            choice = input('choice : ')
            data = {}
            data['choice'] = str(choice)
            data['_uuid'] = uu
            data['_uid'] = uu
            data['_csrftoken'] = self.token
            challnge = self.req.json()['challenge']['api_path']
            self.send = requests.post(f"https://i.instagram.com/api/v1{challnge}", headers=self.headers_login(), data=data, cookies=self.coo)
            contact_point = self.send.json()["step_data"]["contact_point"]
            print(f'code sent to : {contact_point}')
            return self.get_code()
        
        def get_code(self):
            try:
                code = input("code : ")
                data = {}
                data['security_code'] = str(code),
                data['_uuid'] = uu,
                data['_uid'] = uu,
                data['_csrftoken'] = self.token
                path = self.req.json()['challenge']['api_path']
                send_code = requests.post(f"https://i.instagram.com/api/v1{path}", headers=self.headers_login(), data=data, cookies=self.coo)
                if "logged_in_user" in send_code.text:
                    print(f'Login Successfully as @{self.username}')
                    self.coo = send_code.cookies
                    self.token = self.coo.get("csrftoken")
                    self.mid = self.coo.get("mid")
                    self.sessionid = self.coo.get("sessionid")
                    print(f"\n[+] Session ID: {self.sessionid}")
                    print(f"[+] MID: {self.mid}")
                else:
                    regx_error = re.search(r'"message":"(.*?)",', send_code.text).group(1)
                    print(regx_error)
                    ask = input("Code is Not Work Do You Want Try Agin [Y/N] : ")
                    if ask.lower() == "y":
                        time.sleep(1)
                        return self.get_code()
                    else:
                        exit()
            except Exception as e:
                print(f"Error: {e}")
                return self.Login()
            
        def Login(self):
            self.username = input(f'UserName? : ')
            self.DeviceID = self.sesstings.generate_DeviceId(self.username)
            self.passwordd = input(f'Password? : ')
            data = {}
            data['guid'] = uu
            data['enc_password'] = f"#PWD_INSTAGRAM:0:{int(time.time())}:{self.passwordd}"
            data['username'] = self.username
            data['device_id'] = self.DeviceID
            data['login_attempt_count'] = '0'

            self.req = requests.post("https://i.instagram.com/api/v1/accounts/login/", headers=self.headers_login(), data=data)
            if "logged_in_user" in self.req.text:
                print(f'Login Successfully as @{self.username}')
                self.coo = self.req.cookies
                self.token = self.coo.get("csrftoken")
                self.mid = self.coo.get("mid")
                self.sessionid = self.coo.get("sessionid")
                print(f"\n[+] Session ID: {self.sessionid}")
                print(f"[+] MID: {self.mid}")
            elif 'checkpoint_challenge_required' in self.req.text:
                self.coo = self.req.cookies
                self.token = self.coo.get("csrftoken")
                self.mid = self.coo.get("mid")
                self.sessionid = self.coo.get("sessionid")
                print("SCURE FOUND ")
                return self.checkpoint()
            else:
                try:
                    regx_error = re.search(r'"message":"(.*?)",', self.req.text).group(1)
                    print(regx_error)
                except:
                    print(self.req.text)
                ask = input("Something has gone wrong Do You Want Try Agin [Y/N] : ")
                if ask.lower() == "y":
                    time.sleep(1)
                    os.system("cls" if os.name == 'nt' else 'clear')
                    return self.Login()
                else:
                    input()
                    exit()

    login()
    input("\nPress Enter to continue...")



def get_session_acception_code():
    print("="*60)
    print("GET SESSION (ACCEPTIION)")
    print("="*60)

    my_uuid = uuid.uuid4()
    my_uuid_str = str(my_uuid)
    modified_uuid_str = my_uuid_str[:8] + "should_trigger_override_login_success_action" + my_uuid_str[8:]
    rd = ''.join(random.choices(string.ascii_lowercase+string.digits, k=16))
    
    def login(user,password):
        data = {"params": "{\"client_input_params\":{\"contact_point\":\"" + user + "\",\"password\":\"#PWD_INSTAGRAM:0:0:" +  password + "\",\"fb_ig_device_id\":[],\"event_flow\":\"login_manual\",\"openid_tokens\":{},\"machine_id\":\"ZG93WAABAAEkJZWHLdW_Dm4nIE9C\",\"family_device_id\":\"\",\"accounts_list\":[],\"try_num\":1,\"login_attempt_count\":1,\"device_id\":\"android-" + rd + "\",\"auth_secure_device_id\":\"\",\"device_emails\":[],\"secure_family_device_id\":\"\",\"event_step\":\"home_page\"},\"server_params\":{\"is_platform_login\":0,\"qe_device_id\":\"\",\"family_device_id\":\"\",\"credential_type\":\"password\",\"waterfall_id\":\"" + modified_uuid_str + "\",\"username_text_input_id\":\"9cze54:46\",\"password_text_input_id\":\"9cze54:47\",\"offline_experiment_group\":\"caa_launch_ig4a_combined_60_percent\",\"INTERNAL__latency_qpl_instance_id\":56600226400306,\"INTERNAL_INFRA_THEME\":\"default\",\"device_id\":\"android-" + ''.join(random.choices(string.ascii_lowercase+string.digits, k=16)) + "\",\"server_login_source\":\"login\",\"login_source\":\"Login\",\"should_trigger_override_login_success_action\":0,\"ar_event_source\":\"login_home_page\",\"INTERNAL__latency_qpl_marker_id\":36707139}}"}
        data["params"] = data["params"].replace("\"family_device_id\":\"\"", "\"family_device_id\":\"" +my_uuid_str + "\"")
        data["params"] = data["params"].replace("\"qe_device_id\":\"\"", "\"qe_device_id\":\"" + my_uuid_str + "\"")
        headers = {"Host": "i.instagram.com","X-Ig-App-Locale": "ar_SA","X-Ig-Device-Locale": "ar_SA","X-Ig-Mapped-Locale": "ar_AR","X-Pigeon-Session-Id": f"UFS-{uuid.uuid4()}-0","X-Pigeon-Rawclienttime": "1685026670.130","X-Ig-Bandwidth-Speed-Kbps": "-1.000","X-Ig-Bandwidth-Totalbytes-B": "0","X-Ig-Bandwidth-Totaltime-Ms": "0","X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb","X-Ig-Www-Claim": "0","X-Bloks-Is-Layout-Rtl": "true","X-Ig-Device-Id": f"{uuid.uuid4()}","X-Ig-Family-Device-Id": f"{uuid.uuid4()}","X-Ig-Android-Id": f"android-{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}","X-Ig-Timezone-Offset": "10800","X-Fb-Connection-Type": "WIFI","X-Ig-Connection-Type": "WIFI","X-Ig-Capabilities": "3brTv10=","X-Ig-App-Id": "567067343352427","Priority": "u=3","User-Agent": f"Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)","Accept-Language": "ar-SA, en-US","Ig-Intended-User-Id": "0","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Content-Length": "1957","Accept-Encoding": "gzip, deflate","X-Fb-Http-Engine": "Liger","X-Fb-Client-Ip": "True","X-Fb-Server-Cluster": "True"}
        response = requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',headers=headers ,data=data)
        body = response.text
        if "Bearer" in body:
            session = re.search(r'Bearer IGT:2:(.*?),',response.text).group(1).strip()
            session = session[:-8]
            full=base64.b64decode(session).decode('utf-8')
            if "sessionid"  in full:
                sessionid = re.search(r'"sessionid":"(.*?)"}',full).group(1).strip()
                
            print(f"[ + ] Logged in with @{user}")
            print(f"[ + ] Session is : \n{sessionid}")
            input()
            return
        elif "The password you entered is incorrect" in body or "Please check your username and try again." in body or "inactive user" in body or "should_dismiss_loading\", \"has_identification_error\"" in body:
            print("[ - ] Bad Passowrd")
            input()
            return
        elif "challenge_required" in body or "two_step_verification" in body:
            print("[ ! ] Challenge requierd acccept and click enter ")
            input()
            login(user,password)
        else:
            print("[ ! ] Something wrong ")
            input()
            return
    
    USER = str(input("[ + ] Username : "))
    PASSW = str(input("[ + ] Password : "))
    login(USER,PASSW)


def convert_session_web_to_api_code():
    print("="*60)
    print("CONVERT SESSION (WEB TO API)")
    print("="*60)
    
    sessionID = input("SessionId: ")
    auth_payload = '{"ds_user_id":"' + sessionID.split("%3A")[0] + '","sessionid":"' + sessionID + '"}'
    encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')
    headers = {
        "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": f"sessionid={sessionID}",
        "X-Bloks-Version-Id": "5f56efad68e1",
        "X-Bloks-Is-Layout-Rtl": "false",
    }
    req = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true", headers=headers, cookies={"sessionid": sessionID})
    r = req.json()
    mid = req.headers.get("ig-set-x-mid")
    user = r["user"]["username"]
    print("[ DONE ] LOGGED: " + user)
    headers["X-Mid"] = mid
    print("[ DONE ] GET MID: " + mid)
    data = {}
    data['device_id'] = f"android-{''.join(random.choice('1234567890')for i in range(10))}"
    data['authorization_token'] = f"Bearer IGT:2:{encoded_auth}"
    req = requests.post("https://i.instagram.com/api/v1/accounts/continue_as_instagram_login/", headers=headers, data=data)
    if "logged" in req.text:
        print("[ DONE ] CONVERT !")
        sess = req.cookies.get("sessionid")
        if sess == None:
            after = str(base64.b64decode(req.headers.get('ig-set-authorization').split(":")[2]))
            sess = re.search('"sessionid":"(.*?)"',after).groups()[0]
        print("[ API ] Sessionid: " + sess)
    
    input("\nPress Enter to continue...")


def convert_session_web_to_api_via_mid_code():
    print("="*60)
    print("CONVERT SESSION (WEB TO API VIA MID)")
    print("="*60)

    sessionID = input("SessionId: ")
    mid = input("Mid: ")

    auth_payload = '{"ds_user_id":"' + sessionID.split("%3A")[0] + '","sessionid":"' + sessionID + '"}'
    encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')

    headers = {
        "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
        "X-Mid": mid,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": f"sessionid={sessionID}",
        "X-Bloks-Version-Id": "5f56efad68e1",
        "X-Bloks-Is-Layout-Rtl": "false",
    }

    data = {
        'device_id': f"android-{''.join(random.choice('1234567890') for _ in range(10))}",
        'authorization_token': f"Bearer IGT:2:{encoded_auth}"
    }

    req = requests.post("https://i.instagram.com/api/v1/accounts/continue_as_instagram_login/", headers=headers, data=data)

    if "logged" in req.text:
        print("Ok Good")
        sess = req.cookies.get("sessionid")

        if not sess:
            auth_header = req.headers.get('ig-set-authorization')
            if auth_header:
                try:
                    after = base64.b64decode(auth_header.split(":")[2]).decode('utf-8')
                    sess_match = re.search('"sessionid":"(.*?)"', after)
                    if sess_match:
                        sess = sess_match.group(1)
                    else:
                        print("No sessionid found in the decoded response.")
                except (IndexError, ValueError, AttributeError) as e:
                    print(f"Error processing header: {e}")
            else:
                print("The header 'ig-set-authorization' is missing in the response..")

        if sess:
            print("Api SessionID: " + sess)
        else:
            print("Failed to extract SessionID.")
            print(req.text)
    else:
        print("login failed.")
    
    input("\nPress Enter to continue...")

def accept_terms_code():
    print("="*60)
    print("ACCEPT TERMS")
    print("="*60)
    
    sessionid = input("SessionId: ")
    session = sessionid
    headers = {
        "accept": "/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "76",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f'sessionid={session}',
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/terms/unblock/?next=/api/v1/web/fxcal/ig_sso_users/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "viewport-width": "453",
        "x-asbd-id": "198387",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR2BpT3Q3cBoHtz_yRH8EvKCYkOb7loHvR4Jah_iP8s8BmTf",
        "x-instagram-ajax": "9080db6b6a51",
        "x-requested-with": "XMLHttpRequest",
    }
    
    # -------------------------------------------------------------------------
    # FIX: Get CSRF Token dynamically instead of hardcoding
    # -------------------------------------------------------------------------
    try:
        print("[*] Fetching CSRF token from Instagram...")
        req = requests.get("https://www.instagram.com/", cookies={"sessionid": session})
        csrf_token = req.cookies.get("csrftoken")
        
        if not csrf_token:
            # Fallback: Try to find csrf token in response text if not in cookies
            match = re.search(r'"csrf_token":"(.*?)"', req.text)
            if match:
                csrf_token = match.group(1)
            else:
                 # Last resort fallback if we can't get it
                csrf_token = "m2kPFuLMBSGix4E8ZbRdIDyh0parUk5r" 
                print("[!] Could not fetch CSRF token. Using fallback (might fail).")
        else:
            print(f"[+] CSRF Token: {csrf_token}")
            
        headers["x-csrftoken"] = csrf_token
        
    except Exception as e:
        print(f"[!] Error fetching CSRF token: {e}")
        headers["x-csrftoken"] = "m2kPFuLMBSGix4E8ZbRdIDyh0parUk5r" # Fallback
    # -------------------------------------------------------------------------
    data1 = "updates=%7B%22existing_user_intro_state%22%3A2%7D&current_screen_key=qp_intro"
    data2 = "updates=%7B%22tos_data_policy_consent_state%22%3A2%7D&current_screen_key=tos"
    response1 = requests.post("https://www.instagram.com/web/consent/update/", headers=headers, data=data1).text
    response2 = requests.post("https://www.instagram.com/web/consent/update/", headers=headers, data=data2).text
    if '{"screen_key":"finished","status":"ok"}' in response1 or '{"screen_key":"finished","status":"ok"}' in response2:
        print("Success: Terms of Service accepted!")
    else:
        print("Failure: Could not accept Terms of Service.")
    
    input("\nPress Enter to continue...")


def removing_former_users():
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_random_csrf():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def display_header():
        clear_console()
        print("=" * 60)
        print("[!] Before using this option u must remove your acc pfp")
        print("[!] Removing the former may take some time, do not rush.")
        print("=" * 60)
        print()

    def change_profile_picture(sessionid, url_img):
        url = 'https://www.instagram.com/accounts/web_change_profile_picture/'

        csrf_token = generate_random_csrf()
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/edit/",
            "X-CSRFToken": csrf_token,
            "Cookie": f"sessionid={sessionid}; csrftoken={csrf_token};"
        }

        try:
            # Download image
            try:
                image_response = requests.get(url_img, timeout=10)
            except Exception as e:
                return False
            if image_response.status_code != 200:
                return False
                
            files = {
                "profile_pic": ("profile.jpg", image_response.content, "image/jpeg")
            }
            
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200 and response.json().get("status") == "ok":
                return True
            else:
                return False
        except:
            return False

    def login_user():
        display_header()
        sessionid = input("\nEnter your Instagram sessionid: ").strip()
        
        try:
            headers = {
                "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
                "Cookie": f"sessionid={sessionid}"
            }
            
            response = requests.get(
                "https://i.instagram.com/api/v1/accounts/current_user/?edit=true",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json().get('user', {})
                username = user_data.get('username', 'Unknown')
                print(f"\n[+] Logged in as: @{username}")
                time.sleep(2)
                clear_console()
                return sessionid
            else:
                print(f"\n[!] Invalid sessionid. Status: {response.status_code}")
                return None
        except Exception as e:
            print(f"\n[!] Error verifying sessionid: {e}")
            return None

    def change_profile_pictures(sessionid):
        pfp_urls = [
            'https://i.pinimg.com/550x/35/3f/c5/353fc517a4f4fac8d9ecfc734818e048.jpg',
            'https://i.pinimg.com/236x/c1/43/43/c1434392c4c11ac42b782e9397eb2b58.jpg',
            'https://i.pinimg.com/originals/0f/42/27/0f42279ce48796e63c920ba9aa0295a2.jpg',
            'https://i.pinimg.com/236x/bf/8d/0d/bf8d0d9df86c121ad4e9ed65b4bb92cb.jpg'
        ]
        change_count = 0
        error = 0
        display_header()
        
        try:
            while True:
                for url in pfp_urls:
                    success = change_profile_picture(sessionid, url)
                    if success:
                        change_count += 1
                        print(f"- Total changes: [{change_count}], Error: [{error}]     ", end='\r')
                    else:
                        error += 1
                    time.sleep(20)
        except KeyboardInterrupt:
            print(f"\n\n[!] Stopped by user")
            print(f"[+] Total changes: {change_count}")
            print(f"[+] Errors: {error}")

    def main_removing():
        display_header()
        sessionid = login_user()
        if sessionid:
            change_profile_pictures(sessionid)
        else:
            print("\n[!] Exiting. Could not authenticate.")
        
        input("\nPress Enter to continue...")

    main_removing()


def get_account_info():
    print("="*60)
    print("GET ACCOUNT INFO")
    print("="*60)
    
    sessionid = input("\nEnter session ID: ").strip()
    if not sessionid:
        print("[!] Session ID is required!")
        input("\nPress Enter to continue...")
        return
    
    print("\n[*] Getting account info...")
    
    try:
        headers = {
            "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
            "Cookie": f"sessionid={sessionid}"
        }
        
        response = requests.get(
            "https://i.instagram.com/api/v1/accounts/current_user/?edit=true",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json().get('user', {})
            
            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Username: @{user_data.get('username', 'N/A')}")
            print(f"Full Name: {user_data.get('full_name', 'N/A')}")
            print(f"User ID: {user_data.get('pk', 'N/A')}")
            print(f"Email: {user_data.get('email', 'N/A')}")
            print(f"Phone: {user_data.get('phone_number', 'N/A')}")
            print(f"Bio: {user_data.get('biography', 'N/A')}")
            print(f"Followers: {user_data.get('follower_count', 'N/A')}")
            print(f"Following: {user_data.get('following_count', 'N/A')}")
            print(f"Posts: {user_data.get('media_count', 'N/A')}")
            print(f"Private Account: {user_data.get('is_private', 'N/A')}")
            print(f"Verified: {user_data.get('is_verified', 'N/A')}")
            print(f"Business Account: {user_data.get('is_business', 'N/A')}")
            print("="*50)
        else:
            print(f"[!] Failed to get account info. Status: {response.status_code}")
            
    except Exception as e:
        print(f"[!] Error: {str(e)}")
    
    input("\nPress Enter to continue...")


def change_name():
    print("="*60)
    print("CHANGE NAME")
    print("="*60)
    
    print("\nInstagram Name Changer Tool")
    print("-" * 30)
    

    session_id = input("\nEnter your Instagram session ID: ").strip()
    
    if not session_id:
        print("[!] Session ID is required")
        input("\nPress Enter to continue...")
        return
    

    try:
        changer = InstagramNameChanger(session_id)
        print(f"[✓] Tool initialized for user_id: {changer.user_id}")
        

        print("\nChecking current name...")
        current_name_info = changer.get_current_name()
        
        if current_name_info["success"]:
            current_name = current_name_info["current_name"]
            if current_name:
                print(f"[i️] Current name: '{current_name}'")
            else:
                print(f"[i️] Current name: (empty)")
        else:
            print(f"Could not retrieve current name: {current_name_info.get('error', 'Unknown error')}")
        

        print("\nSelect operation:")
        print("1.  Set a new name")
        print("2.  Remove current name")
        print("3.  Change multiple names")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":

            new_name = input("\nEnter new name: ").strip()
            if new_name:
                result = changer.update_profile_name(new_name)
                
                if result.get("success"):
                    print(f"\n{result.get('message', 'Operation completed successfully!')}")
                else:
                    print(f"\nFailed: {result.get('error', 'Unknown error')}")
            else:
                print("[!] New name is required")
        
        elif choice == "2":

            confirm = input("\nAre you sure you want to remove the current name? (y/n): ").strip().lower()
            if confirm == 'y':
                result = changer.update_profile_name("")   
                
                if result.get("success"):
                    print(f"\n{result.get('message', 'Name removed successfully!')}")
                else:
                    print(f"\nFailed: {result.get('error', 'Unknown error')}")
            else:
                print("[!] Operation cancelled")
        
        elif choice == "3":
          
            print("\nEnter names (one per line, type 'done' to finish):")
            names = []
            while True:
                name = input(f"Name {len(names)+1}: ").strip()
                if name.lower() == 'done':
                    break
                if name:
                    names.append(name)
            
            if names:
                delay = input("\nEnter delay between changes (seconds, default 5): ").strip()
                delay_seconds = int(delay) if delay.isdigit() else 5
                
                changer.batch_update_names(names, delay_seconds)
            else:
                print("[!] No names entered")
        
        else:
            print("[!] Invalid option")
    
    except Exception as e:
        print(f"[!] Error running the tool: {e}")
    
    input("\nPress Enter to continue...")


def change_bio_code():
    print("="*60)
    print("CHANGE BIO")
    print("="*60)
    
    def update_bio(Sessionid, Bio):
        try:
            auth_payload = '{"ds_user_id":"' + Sessionid.split("%3A")[0] + '","sessionid":"' + Sessionid + '"}'
            encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')
            headers = {}
            headers['User-Agent'] =  "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)"
            headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers["Authorization"] = f"Bearer IGT:2:{encoded_auth}"
            req = requests.request("POST", "https://i.instagram.com/api/v1/accounts/set_biography/", headers=headers, data="raw_text=" + Bio)
            if '"ok"' in req.text:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    sessionid = input("Enter API Session ID: ").strip()
    bio_text = input("Enter new bio text: ").strip()
    
    if update_bio(sessionid, bio_text):
        print("✅ Bio changed successfully!")
    else:
        print("❌ Failed to change bio")
    
    input("\nPress Enter to continue...")


def reset_password_inactive_acc():
    print("="*60)
    print("RESET PW (INACTIVE ACC)")
    print("="*60)
    
    INSTAGRAM_API = "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/"

    def random_id(prefix="android-"):
        return prefix + uuid.uuid4().hex[:16]

    def gen_headers():
        return {
            "host": "i.instagram.com",
            "x-ig-app-locale": "en_OM",
            "x-ig-device-locale": "en_OM",
            "x-ig-mapped-locale": "en_AR",
            "x-pigeon-session-id": f"UFS-{uuid.uuid4()}-1",
            "x-pigeon-rawclienttime": str(time.time()),
            "x-ig-bandwidth-speed-kbps": str(random.randint(300, 1000)) + ".000",
            "x-ig-bandwidth-totalbytes-b": str(random.randint(1_000_000, 5_000_000)),
            "x-ig-bandwidth-totaltime-ms": str(random.randint(3000, 10000)),
            "x-bloks-version-id": "5f56efad68e1",
            "x-ig-www-claim": "0",
            "x-bloks-is-layout-rtl": "true",
            "x-ig-device-id": str(uuid.uuid4()),
            "x-ig-family-device-id": str(uuid.uuid4()),
            "x-ig-android-id": random_id(),
            "x-ig-timezone-offset": "14400",
            "x-fb-connection-type": "WIFI",
            "x-ig-connection-type": "WIFI",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-app-id": "567067343352427",
            "priority": "u=3",
            "user-agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
            "accept-language": "en-OM, en-US",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "accept-encoding": "zstd, gzip, deflate",
            "x-fb-http-engine": "Liger",
            "ig-intended-user-id": "0",
        }

    def send_recovery(email_or_username):
        if not email_or_username:
            return {"error": "Missing email_or_username"}

        body_json = {
            "adid": str(uuid.uuid4()),
            "guid": str(uuid.uuid4()),
            "device_id": random_id(),
            "query": email_or_username,
            "waterfall_id": str(uuid.uuid4())
        }

        signed_body = "SIGNATURE." + json.dumps(body_json, separators=(",", ":"))

        data = {"signed_body": signed_body}

        headers = gen_headers()

        try:
            r = requests.post(INSTAGRAM_API, headers=headers, data=data)
            return {"status": r.status_code, "response": r.text.replace('\\','')}
        except Exception as e:
            return {"error": str(e)}

    print("Instagram Recovery Tool | By @suul \n")
    user = input("put ur username : ")
    result = send_recovery(user)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    input("\nPress Enter to continue...")

def reset_password_active_acc():
    print("="*60)
    print("RESET PW (ACTIVE ACC)")
    print("="*60)
    
    class Xnce():
        def __init__(self):
            print(f"\n[+] Target: ", end="")
            self.target = input().strip()
            
            if not self.target:
                print("[!] No target provided!")
                return
            
            if self.target.startswith("@"):
                print(f"\n[!] Enter username without @")
                self.target = self.target[1:]  # Remove @ if present
            
            if "@" in self.target:
                usem = "user_email"
            else:
                usem = "username"
            
            self.data = {
                "_csrftoken": "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)),
                usem: self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }
            self.send_password_reset()
            
        def send_password_reset(self):
            print(f"\n[*] Sending password reset request for: {self.target}")
            
            head = {"user-agent": f"Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)"}
            
            try:
                req = requests.post("https://i.instagram.com/api/v1/accounts/send_password_reset/", 
                                  headers=head, 
                                  data=self.data,
                                  timeout=10)
                
                print(f"[*] Status Code: {req.status_code}")
                
                if req.status_code == 200:
                    try:
                        response_json = req.json()
                        if "obfuscated_email" in req.text or "email" in req.text:
                            print(f"\n[✅] SUCCESS! Password reset email sent!")
                            print(f"[📧] Check the email associated with the account")
                            print(f"[📱] Response: {response_json}")
                        elif "message" in response_json and "No users found" in response_json["message"]:
                            print(f"\n[❌] FAILED! No user found with: {self.target}")
                        else:
                            print(f"\n[⚠️] Response: {response_json}")
                    except:
                        if "obfuscated_email" in req.text:
                            print(f"\n[✅] SUCCESS! Password reset email sent!")
                        else:
                            print(f"\n[📝] Raw Response: {req.text[:200]}...")
                
                elif req.status_code == 404:
                    print(f"\n[❌] FAILED! User not found: {self.target}")
                
                elif req.status_code == 400:
                    print(f"\n[❌] BAD REQUEST! Check the username/email format")
                
                elif req.status_code == 429:
                    print(f"\n[⚠️] RATE LIMITED! Too many requests, try again later")
                
                else:
                    print(f"\n[❌] FAILED! Status: {req.status_code}")
                    print(f"[📝] Response: {req.text[:200]}...")
                    
            except requests.exceptions.Timeout:
                print(f"\n[❌] TIMEOUT! Request timed out")
            except requests.exceptions.ConnectionError:
                print(f"\n[❌] CONNECTION ERROR! Check your internet")
            except Exception as e:
                print(f"\n[❌] ERROR: {str(e)}")
    
    Xnce()
    input("\nPress Enter to continue...")

def skipping_dismiss_code():
    print("="*60)
    print("SKIPPING DISMISS")
    print("="*60)
    
    sessionid = input("Sessionid: ")
    auth_payload = '{"ds_user_id":"' + sessionid.split("%3A")[0] + '","sessionid":"' + sessionid + '"}'
    encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')
    headers = {
        "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": f"sessionid={sessionid}",
        "Authorization": f"Bearer IGT:2:{encoded_auth}",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": "UFS-ac8724b2-4fe9-42ac-a47c-9a08f0ec51d4-0",
        "X-Pigeon-Rawclienttime": "1689682437.583",
        "X-Ig-Bandwidth-Speed-Kbps": "17585.000",
        "X-Ig-Bandwidth-Totalbytes-B": "11739493",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "5f56efad68e1",
        "X-Ig-Www-Claim": "hmac.AR1HYidj0VZt3cEDHC_CDLJm9Zil8u1vS2gb0Mgb7b4Gn4Qx",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": "3bc694b1-e663-4689-af50-c57ae12342d7",
        "X-Ig-Family-Device-Id": "48dc9c78-bd01-4deb-8a7f-ea77f8a9c173",
        "X-Ig-Android-Id": "android-6b9bd681ae255c63",
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "SelfFragment:self_profile:14:main_profile:1689682239.541::,ProfileMediaTabFragment:self_profile:15:button:1689682239.979::,EditProfileFragment:edit_profile:16:button:1689682250.31::,ProfileMediaTabFragment:self_profile:20:button:1689682334.434::,EditProfileFragment:edit_profile:21:button:1689682342.179::,ProfileMediaTabFragment:self_profile:23:button:1689682409.62::,ProfileMenuFragment:bottom_sheet_profile:24:button:1689682410.206::,ProfileMediaTabFragment:self_profile:25:button:1689682413.169::,ProfileMenuFragment:bottom_sheet_profile:26:button:1689682413.354::,com.instagram.portable_settings.settings:com.instagram.portable_settings.settings:27:button:1689682414.763::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "Accept-Language": "en-US",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True"
    }
    Check = requests.get('https://www.instagram.com/api/v1/challenge/web/', params={'next': '/_n/emaillogindlink%3Fuid%3D1tz1p2w%26token%3DdFBV7z%26auto_send%3D0%26is_caa%3D1',}, headers=headers)
    if "We suspect automated behavior on your account" in Check.text:
        print("THIS IS DISMISS MESSAGE")
        match = re.search(r'"challenge_context":"([^"]+)"', Check.text)
        challenge_context = match.group(1)
        data = {
            "challenge_context": challenge_context,
            "has_follow_up_screens": "false",
            "nest_data_manifest": "true"
        }
        response = requests.post("https://www.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/", headers=headers, data=data)
        print("DONE SKIP MESSAGE ! ")
    else:
        print("NOT FOUND DISMISS MESSAGE")
    
    input("\nPress Enter to continue...")


def sessions_validator_code():
    print("="*60)
    print("SESSIONS VALIDATOR")
    print("="*60)
    
    def get_csrf_token(session_id):
        try:
            # First try: Make a lightweight request to get cookies
            response = requests.get("https://www.instagram.com/", cookies={"sessionid": session_id})
            token = response.cookies.get("csrftoken")
            encoded_token = response.cookies.get("csrftoken") # sometimes encoded differently
            
            if token:
                return token
            
            # Second try: Look in response text if not in cookies
            match = re.search(r'"csrf_token":"(.*?)"', response.text)
            if match:
                return match.group(1)
            
            return "".join(random.choices(string.ascii_letters + string.digits, k=32)) # Fallback
            
        except:
             return "".join(random.choices(string.ascii_letters + string.digits, k=32)) # Fallback

    def get_headers(session_id, type_):
        if type_ == "info":
            device_id = f"android-{uuid.uuid4().hex[:16]}"
            return {
                "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
                "Accept": "/",
                "Cookie": f"sessionid={session_id}",
                "Accept-Language": "en-US",
                "Accept-Encoding": "gzip, deflate",
                "X-IG-Capabilities": "3brTvw==",
                "X-IG-Connection-Type": "WIFI",
                "X-IG-App-ID": "567067343352427",
                "X-IG-Device-ID": device_id,
                "X-IG-Android-ID": device_id
            }
        else:
            return {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "x-csrftoken": get_csrf_token(session_id),
                "x-web-session-id": "vsoplz:jg4v4g:fdi5ne",
                "Accept-Language": "en-US",
                "X-IG-App-ID": "567067343352427",
                "Cookie": f"sessionid={session_id}"
            }

    def get_user_info(session_id):
        try:
            headers = get_headers(session_id, "info")
            response = requests.get(
                "https://i.instagram.com/api/v1/accounts/current_user/?edit=true",
                headers=headers
            )
            if response.status_code == 200:
                return response.json()['user']
            else:
                print(f"[!] Failed to fetch user info: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            print(f"[!] Error: {str(e)}")
            return None

    def validate_single_session():
        print("\n" + "="*50)
        print("SINGLE SESSION VALIDATION")
        print("="*50)
        
        session_id = input("Enter session ID: ").strip()
        
        if not session_id:
            print("[!] No session ID provided!")
            return
        
        print("\n[*] Validating session...")
        
        user_info = get_user_info(session_id)
        
        if user_info:
            print("\n[✅] SESSION IS VALID!")
            print(f"[📱] Username: @{user_info.get('username', 'N/A')}")
            print(f"[👤] Full Name: {user_info.get('full_name', 'N/A')}")
            print(f"[📧] Email: {user_info.get('email', 'N/A')}")
            print(f"[📞] Phone: {user_info.get('phone_number', 'N/A')}")
            print(f"[🆔] User ID: {user_info.get('pk', 'N/A')}")
            print(f"[👥] Followers: {user_info.get('follower_count', 'N/A')}")
            print(f"[📊] Following: {user_info.get('following_count', 'N/A')}")
        else:
            print("\n[❌] SESSION IS INVALID OR EXPIRED!")

    def validate_multi_sessions():
        print("\n" + "="*50)
        print("MULTI SESSIONS VALIDATION")
        print("="*50)
        
        filename = input("Enter filename containing sessions: ").strip()
        
        if not filename:
            print("[!] No filename provided!")
            return
        
        if not os.path.exists(filename):
            print(f"[!] File '{filename}' not found!")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                sessions = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"[!] Error reading file: {e}")
            return
        
        if not sessions:
            print("[!] No sessions found in file!")
            return
        
        print(f"\n[*] Found {len(sessions)} sessions to validate...")
        
        valid_sessions = []
        invalid_sessions = []
        
        for i, session in enumerate(sessions, 1):
            print(f"[{i}/{len(sessions)}] Validating session...", end='\r')
            
            user_info = get_user_info(session)
            
            if user_info:
                username = user_info.get('username', 'Unknown')
                valid_sessions.append({
                    'session': session,
                    'username': username,
                    'user_id': user_info.get('pk', 'N/A')
                })
                print(f"[{i}/{len(sessions)}] ✅ Valid: @{username}")
            else:
                invalid_sessions.append(session)
                print(f"[{i}/{len(sessions)}] ❌ Invalid session")
        

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        valid_filename = f"valid_sessions_{timestamp}.txt"
        invalid_filename = f"invalid_sessions_{timestamp}.txt"
        

        with open(valid_filename, 'w', encoding='utf-8') as f:
            for item in valid_sessions:
                f.write(f"Session: {item['session']}\n")
                f.write(f"Username: @{item['username']}\n")
                f.write(f"User ID: {item['user_id']}\n")
                f.write("-" * 50 + "\n")
        

        with open(invalid_filename, 'w', encoding='utf-8') as f:
            for session in invalid_sessions:
                f.write(f"{session}\n")
        
        print("\n" + "="*50)
        print("VALIDATION COMPLETED!")
        print("="*50)
        print(f"✅ Valid sessions: {len(valid_sessions)}")
        print(f"❌ Invalid sessions: {len(invalid_sessions)}")
        print(f"📁 Valid sessions saved to: {valid_filename}")
        print(f"📁 Invalid sessions saved to: {invalid_filename}")

    while True:
        print("\n" + "="*50)
        print("SESSIONS VALIDATOR MENU")
        print("="*50)
        print("1 - SINGLE SESSION")
        print("2 - MULTI SESSIONS (FROM FILE)")
        print("3 - Back to Main Menu")
        print("="*50)
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            validate_single_session()
        elif choice == '2':
            validate_multi_sessions()
        elif choice == '3':
            print("\n[*] Returning to main menu...")
            break
        else:
            print("\n[!] Invalid choice! Please select 1, 2, or 3.")
        
        input("\nPress Enter to continue...")



def random_user_pass_mail_code():
    print("="*60)
    print("RANDOM USER,PASS,MAIL (UNCREATED ACC)")
    print("="*60)
    
    def generate_random_username(length=10):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    def generate_random_password(length=12):
        characters = string.ascii_letters + string.digits + '!@#$%'
        return ''.join(random.choice(characters) for i in range(length))

    def generate_random_email():
        username_length = random.randint(15, 20)
        username = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(username_length))
        
        while username[0].isdigit():
            username = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(username_length))
        
        return f"{username}@gmail.com"

    print("Starting random data generator...")
    
    print("\nGenerating random data...")
    username = generate_random_username()
    password = generate_random_password()
    email = generate_random_email()
    
    print("\n" + "=" * 50)
    print("Generated Data:")
    print("=" * 50)
    print(f"user: {username}")
    print(f"pass: {password}")
    print(f"email: {email}")
    print(f"Email length: {len(email.split('@')[0])} characters")
    print(f"session: ")
    print("=" * 50)
    

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"generated_data_{timestamp}.txt", "w") as f:
        f.write(f"user: {username}\n")
        f.write(f"pass: {password}\n")
        f.write(f"email: {email}\n")
        f.write(f"session: \n")
    
    print(f"\n[+] Data saved to: generated_data_{timestamp}.txt")
    print("\nProgram completed")
    
    input("\nPress Enter to continue...")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_console()
    print("=" * 70)
    print("INSTAGRAM MULTI-TOOL V3.01")
    print(" By: @suul community team")
    print("=" * 70)
    print()
    print("SESSION TOOLS:")
    print(" 1. GET SESSION (CODE)")
    print(" 2. GET SESSION (ACCEPTIION)")
    print(" 4. CONVERT SESSION (WEB TO API)")
    print(" 5. CONVERT SESSION (WEB TO API VIA MID)")
    print(" 6. ACCEPT TERMS")
    print()
    print("ACCOUNT MANAGEMENT:")
    print(" 7. REMOVING FORMER USERS")
    print(" 8. GET ACCOUNT INFO")
    print(" 9. CHANGE NAME")
    print("10. CHANGE BIO")
    print()
    print("PASSWORD RESET:")
    print("13. RESET PW (INACTIVE ACC)")
    print("14. RESET PW (ACTIVE ACC)")
    print()
    print("OTHER TOOLS:")
    print("15. SKIPPING DISMISS")
    print("16. SESSIONS VALIDATOR")
    print("17. RANDOM USER,PASS,MAIL")
    print()
    print(" 0. EXIT")
    print("=" * 70)


choices = {
    '1': get_session_code,
    '2': get_session_acception_code,
    '4': convert_session_web_to_api_code,
    '5': convert_session_web_to_api_via_mid_code,
    '6': accept_terms_code,
    '7': removing_former_users,
    '8': get_account_info,
    '9': change_name,
    '10': change_bio_code,
    '13': reset_password_inactive_acc,
    '14': reset_password_active_acc,
    '15': skipping_dismiss_code,
    '16': sessions_validator_code,
    '17': random_user_pass_mail_code,
}

def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (0-17, skip 3&11&12): ").strip()
        
        if choice == '0':
            print("\nExiting the program. Goodbye!")
            break
        
        if choice in choices:
            try:
                choices[choice]()
            except Exception as e:
                print(f"\n[!] Error executing function: {e}")
                input("\nPress Enter to continue...")
        else:
            print("\n[!] Invalid choice. Please enter a valid number from the menu.")
            print("[!] Note: Options 11 and 12 are not available.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
