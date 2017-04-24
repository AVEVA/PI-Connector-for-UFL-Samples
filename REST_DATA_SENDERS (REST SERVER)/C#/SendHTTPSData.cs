using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace HttpPostUFLTest
{
    class Program
    {
        // Configure following properties according to your DataSource configuration
        static string uriAddress = "https://host:5460/connectordata/DataSourceName/";
        static string user = "username";
        static string password = "password";

        // Stream of characters what should be sent via REST
        static string data = "data";

        static void Main(string[] args)
        {
            SendHttpsDataPUT();
            SendHttpsDataPOST();
            Console.ReadKey();
        }

        static void SendHttpsDataPUT()
        {
            byte[] fileToSend = Encoding.UTF8.GetBytes(data);

            System.Net.ServicePointManager.ServerCertificateValidationCallback = new System.Net.Security.RemoteCertificateValidationCallback(
            (object sender, X509Certificate certification, X509Chain chain, SslPolicyErrors sslPolicyErrors) => { return true; });
            using (var wb = new WebClient())
            {
                string svcCredentials = Convert.ToBase64String(ASCIIEncoding.ASCII.GetBytes(user + ":" + password));
                wb.Headers[HttpRequestHeader.Authorization] = string.Format("Basic {0}", svcCredentials);
                try
                {
                    var response = wb.UploadData(uriAddress, "PUT", fileToSend);
                    string sResponse = Encoding.ASCII.GetString(response);
                    Console.WriteLine(sResponse);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }

        static void SendHttpsDataPOST()
        {
            uriAddress = uriAddress + "POST";
            byte[] fileToSend = Encoding.UTF8.GetBytes(data);

            System.Net.ServicePointManager.ServerCertificateValidationCallback = new System.Net.Security.RemoteCertificateValidationCallback(
            (object sender, X509Certificate certification, X509Chain chain, SslPolicyErrors sslPolicyErrors) => { return true; });
            using (var wb = new WebClient())
            {
                string svcCredentials = Convert.ToBase64String(ASCIIEncoding.ASCII.GetBytes(user + ":" + password));
                wb.Headers[HttpRequestHeader.Authorization] = string.Format("Basic {0}", svcCredentials);
                try
                {
                    var response = wb.UploadData(uriAddress, "POST", fileToSend);
                    string sResponse = Encoding.ASCII.GetString(response);
                    Console.WriteLine(sResponse);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}
