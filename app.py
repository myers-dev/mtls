from flask import Flask
from flask import request
from flask import render_template

from cryptography import x509
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

@app.route("/")
def mTLS():

    pem_data = "--- No Header is detected ---"
    cert_fields = {}

    if 'X-Arr-Clientcert' in request.headers.keys():

        header = str(request.headers['X-Arr-Clientcert'])
        
        pem_data = f"-----BEGIN CERTIFICATE-----{header}-----END CERTIFICATE-----"
        
        cert = x509.load_pem_x509_certificate(str.encode(pem_data), default_backend())

        cert_fields = {}
        fields = [  'issuer', 'not_valid_after', 'not_valid_before', 'serial_number', 'subject', 'version']
        for field in fields:
            try:
                cert_fields[field] = getattr(cert,field)
            except Exception as error:
                pass

    return render_template('headers.html', headers=request.headers, pem_data = pem_data , cert_fields = cert_fields )

@app.route("/healthz")
def healthz():
    return render_template('healthz.html');