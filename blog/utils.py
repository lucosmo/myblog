from ipware import get_client_ip as ipware_get_client_ip

def get_client_ip(request):
    client_ip, is_routable = ipware_get_client_ip(request)
    if client_ip:
        return client_ip
    else:
        return '0.0.0.0'