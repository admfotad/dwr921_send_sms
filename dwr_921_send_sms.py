import requests
import sys

def main():

    class DWR921_sms:
        def __init__(self,IP,login,pasw):
            self.ip=IP
            self.user=login
            self.password=pasw

        def import_module(self,module):
            import os
            try:
                import module
            except ImportError:
                try:
                    to_install='pip install {} || easy_install {}'.format(module,module)
                    os.system(to_install)
                except:
                    return None

        def prepare_url(self):
            return 'http://{}/log/in?un={}&pw={}&rd=%2Fuir%2Fstatus.htm&rd2=%2Fuir%2Fwanst.htm&Nrd=1'.format(self.ip,self.user,self.password)

        def router_login(self):
            s = requests.Session()
            url=self.prepare_url()
            try:
                resp=s.get(url,verify=False)
                if resp.status_code==200:
                    return s.cookies
                else:
                    return None
            except Exception as e:
                print(e)
                sys.exit(-1)

        def send_sms(self,pnumber,text):
            cookies=self.router_login()
            if cookies is not None:
                s = requests.Session()
                url='http://{}/smsmsg.htm?Nsend=1&Nmsgindex=0&S801E2700={}&S801E2800={}'.format(self.ip,pnumber,text)
                resp=s.get(url,cookies=cookies)
                url='http://{}/sms2.htm?Ncmd=2'.format(self.ip)
                resp=s.get(url,cookies=cookies)
                return resp.status_code
            else:
                return None


    f=DWR921_sms('IP_address','ausername','password')
    print(f.send_sms('phone_number','sms_text'))


if __name__ == '__main__':
    main()
