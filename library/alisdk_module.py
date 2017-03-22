__author__ = 'pangff'
from ansible.module_utils.basic import *
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import UploadServerCertificateRequest


def initClient(module):
   clt = client.AcsClient(module.params['AccessKeyID'], module.params['AccessKeySecret'], module.params['RegionId'])
   return clt

def uploadServerCertificate(clt,module):
    request = UploadServerCertificateRequest.UploadServerCertificateRequest()
    request.set_ServerCertificate(module.params['ServerCertificate'])
    request.set_PrivateKey(module.params['PrivateKey'])
    request.set_ServerCertificateName("alisdk_module")
    request.set_accept_format(module.params["Format"])
    result = clt.do_action(request)
    return json.loads(result);


def main():
    fields = {
        "AccessKeyID": {"required": True, "type": "str"},
        "AccessKeySecret": {"required": True, "type": "str"},
        "Version": {"required": True, "type": "str"},
        "Format": {"required": True, "type": "str"},
        "SignatureVersion":{"required": True, "type": "str"},
        "ResourceOwnerAccount":{"required": True, "type": "str"},
        "Action": {"required": True, "type": "str"},
        "RegionId": {"required": True, "type": "str"},
        "ServerCertificate": {"required": True, "type": "str"},
        "ServerCertificateName": {"required": True, "type": "str"},
        "PrivateKey": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    clt = initClient(module);
    result = uploadServerCertificate(clt,module);
    response = {"result":result}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()