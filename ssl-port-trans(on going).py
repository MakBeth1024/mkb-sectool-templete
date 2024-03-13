import datetime
import random
import ssl
import string
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

password = b'MakBeth'


def random_string(length: int) -> str:
    """
    定长随机字符串
    """
    charset = string.ascii_letters + string.digits
    return ''.join(random.choices(charset, k=length))


def create_self_signed_cert():
    '''
    生成私钥
    '''
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, random_string(6) + ".com")
        # x509.NameAttribute(NameOID.COUNTRY_NAME, u"US" ),
        # x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        # x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco" ),
        # x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company" ),
        # x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
    ])

    # 创建证书的基本配置
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        1000
        # x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(
        private_key=private_key,
        algorithm=hashes.SHA256()
    )

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    # 将证书保存到文件

    with open("cert_file.pem", "wb") as fc:
        fc.write(cert.public_bytes(
            serialization.Encoding.PEM
        ))

    # 将私钥保存到文件
    with open("key_file.pem", "wb") as fk:
        fk.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))

    return cert_pem, key_pem

    # 将证书保存到文件

    # with open(cert,"wb") as f:
    #     f.write(cert.public_bytes(
    #         serialization.Encoding.PEM
    #     ))
    # 将私钥保存到文件
    # with open(key_file,"wb")as f:
    #     f.write(private_key.private_bytes(
    #         serialization.Encoding.PEM,
    #         serialization.PrivateFormat.PKCS8,
    #         serialization.NoEncryption()
    #     ))


def config() -> ssl.SSLContext:
    """
    配置SSL上下文
    """
    cert_pem, key_pem = create_self_signed_cert()

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
    context.set_ciphers("ECDHE+AESGCM")
    context.load_cert_chain(
        certfile='cert_file.pem',
        keyfile='key_file.pem',
        password=None
    )
    # context.load_cert_chain(certfile=None, keyfile=None, cert_data=cert_pem)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # print(cert_pem, key_pem)

    return context


if __name__ == "__main__":
    config()


