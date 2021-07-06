import requests
import sys
import json

domains = {"thetruthspy.com": ["protocol-a720",
                               "protocol-a721",
                               "protocol-a723",
                               "protocol-a726",
                               "protocol-a722",
                               "protocol-a724",
                               "protocol-a725",
                               "protocol-a742",
                               "protocol-a727",
                               "protocol-a728",
                               "protocol-a729",
                               "protocol-a730",
                               "protocol-a735",
                               "protocol-a736",
                               "protocol-a737",
                               "protocol-a731",
                               "protocol-a732",
                               "protocol-a733",
                               "protocol-a734",
                               "protocol-a740",
                               "protocol-a738",
                               "protocol-a739",
                               "protocol-a741",
                               "protocol-a743",
                               "protocol-a744",
                               "protocol-a745",
                               "protocol-a746",
                               "protocol-a747",
                               "media-sync-a743",
                               "media-sync-a920.",
                               "media-sync-a830",
                               "media-sync-a940",
                               "media-sync-a925",
                               "media-sync-a935",
                               "media-sync-a910",
                               "media-sync-a915",
                               "media-sync-a930",
                               "media-sync-a747",
                               "media-sync-a746",
                               "media-sync-a810"],
           "copy9.com":   ["media-sync-a618",
                           "media-sync-a620",
                           "media-sync-a621",
                           "media-sync-a696",
                           "protocol-a",
                           "protocol-a610",
                           "protocol-a611",
                           "protocol-a612",
                           "protocol-a614",
                           "protocol-a615",
                           "protocol-a616",
                           "protocol-a617",
                           "protocol-a618",
                           "protocol-a620",
                           "protocol-a621",
                           "protocol-a69",
                           "protocol-a696",
                           "protocol-a710",
                           "protocol-a780",
                           "protocol-viewer-a",
                           "protocol",
                           "media-sync-a710",
                           "media-sync-a780"]
           }


def check_imei(imei):

    results = {}
    for domain, subs in domains.items():
        for sub in subs:
            try:
                path = "/protocols/check_device_registered.aspx?deviceid="
                res = requests.get("http://{}.{}{}{}".format(sub, domain, path, imei),
                                   proxies=dict(
                    http='socks5://localhost:9050',
                    https='socks5://localhost:9050'),
                    timeout=3)
                if "The device does not exist in the system." in res.content.decode('utf8'):
                    results[domain] = False
                    break
                elif "deviceid" in res.content.decode('utf8'):
                    results[domain] = True
                    break
            except:
                pass

    return json.dumps(results)


if __name__ == "__main__":
    try:
        assert (int(sys.argv[1]) and len(sys.argv[1]) == 15)
        print(check_imei(sys.argv[1]))
    except:
        print("Please specify an IMEI")
