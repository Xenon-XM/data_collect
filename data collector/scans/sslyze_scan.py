from sslyze import (
    ServerNetworkLocationViaDirectConnection,
    ServerConnectivityTester,
    Scanner,
    ServerScanRequest,
    ScanCommand, 
)
from sslyze.errors import ConnectionToServerFailed
from cryptography import x509
from cryptography.x509 import NameOID
from typing import List

def get_common_names(name_field: x509.Name) -> List[str]:
    return [cn.value for cn in name_field.get_attributes_for_oid(NameOID.COMMON_NAME)]

def _get_name_as_short_text(name_field: x509.Name) -> str:
    """Convert a name field returned by the cryptography module to a string suitable for displaying it to the user.
    """
    # Name_field is supposed to be a Subject or an Issuer; print the CN if there is one
    common_names = get_common_names(name_field)
    if common_names:
        # We don't support certs with multiple CNs
        return common_names[0]
    else:
        # Otherwise show the whole field
        return name_field.rfc4514_string()
        
class SSlyzeScanner:
    def __init__(self):
        self.cert = False
        self.issuer = None
        self.num_certificates = None
    def test(self, target):
        targer = target
        try:
            server_location = ServerNetworkLocationViaDirectConnection.with_ip_address_lookup(target, 443)
            try:
                server_info = ServerConnectivityTester().perform(server_location)
                scanner = Scanner()
                all_server_scans = [
                    ServerScanRequest(
                    server_info=server_info, scan_commands={ScanCommand.CERTIFICATE_INFO}
                    )
                ]
                scanner.start_scans(all_server_scans)
                for server_scan_result in scanner.get_results():
                    try:
                        certinfo_result = server_scan_result.scan_commands_results[ScanCommand.CERTIFICATE_INFO]
                        #print("\nNumber of certificates detected:"+ str(len(certinfo_result.certificate_deployments))+"\n")
                        self.num_certificates = str(len(certinfo_result.certificate_deployments))
                        cert_deployment = certinfo_result.certificate_deployments[0]
                        leaf_certificate = cert_deployment.received_certificate_chain[0]
                        try:
                            final_issuer_field = _get_name_as_short_text(leaf_certificate.issuer)
                        except ValueError:
                            # Cryptography could not parse the certificate https://github.com/nabla-c0d3/sslyze/issues/495
                            final_issuer_field = "Issuer could not be parsed"
                        self.issuer = final_issuer_field
                    except KeyError:
                        self.issuer = None
                        self.num_certificates = None
                        pass
                self.cert = True
            except ConnectionToServerFailed as e:
                pass
        except:
            pass
        
