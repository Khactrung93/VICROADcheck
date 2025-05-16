import requests
import json
from datetime import datetime


# === Cấu hình của bạn ===
TELEGRAM_BOT_TOKEN = "8060947068:AAFwKFJ_7Fh8iojnP0pJdu4tjKAOM9CNBy4"
TELEGRAM_CHAT_ID = "6037054601"
YOUR_DATE = "2025-05-28"  # Ngày bạn muốn so sánh (định dạng: YYYY-MM-DD)

# === Thông tin request lấy JSON từ Looker Studio ===
url = "https://lookerstudio.google.com/embed/u/0/batchedDataV2?appVersion=20250425_0200"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5",
    "content-type": "application/json",
    "origin": "https://lookerstudio.google.com",
    "referer": "https://lookerstudio.google.com/embed/u/0/reporting/5513a22b-6546-4435-94a7-b00d37cfeae1/page/p_bjphlvetcd",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "x-client-data": "CI22yQEIorbJAQipncoBCJnoygEIlKHLAQiSo8sBCIWgzQEIucjNAQjGzc4BCJ3tzgEI5O3OAQjd7s4B",
    "x-rap-xsrf-token": "AImk1AKXqN70Ab-sOEh-4yfWzEdgG3lcdg:1747391486296",
}

cookies = {
    # Dán toàn bộ cookies lấy từ cURL vào đây, ví dụ:
    # "RAP_XSRF_TOKEN": "...",
    # ...
    "RAP_XSRF_TOKEN": "AImk1AKXqN70Ab-sOEh-4yfWzEdgG3lcdg:1747391486296",
    "HSID": "AQv__Nxsp_Dx8J3IP",
    "SSID": "AzeIK_MGxEX2raqaX",
    "APISID": "63ro8FeNlfHPCq0G/Ao82Q_iNRjhgPQ24k",
    "SAPISID": "wn-_6ONd3KJeJEpJ/ATYLZrOKQQ03Cqu1t",
    "__Secure-1PAPISID": "wn-_6ONd3KJeJEpJ/ATYLZrOKQQ03Cqu1t",
    "__Secure-3PAPISID": "wn-_6ONd3KJeJEpJ/ATYLZrOKQQ03Cqu1t",
    "SEARCH_SAMESITE": "CgQIzJ0B",
    "SID": "g.a000wQiPPGC9lPuLqojiU14B0MAHOU2wQbonkF5AJbeIhUYpw-llxe51WUiQlEdALjxbR2zERwACgYKAbUSARISFQHGX2MiG9reSLuPyy1OUK-IS490aRoVAUF8yKrLkF9O7qnChZUy7Pt2mThP0076",
    "__Secure-1PSID": "g.a000wQiPPGC9lPuLqojiU14B0MAHOU2wQbonkF5AJbeIhUYpw-llY6-wvFrJpvJ7SV-m1wuImQACgYKASYSARISFQHGX2MibaTGm4xTdj7sKyYEw3eNkhoVAUF8yKquX3DQZx3AUjTezJ74bDh20076",
    "__Secure-3PSID": "g.a000wQiPPGC9lPuLqojiU14B0MAHOU2wQbonkF5AJbeIhUYpw-ll3KIoV4hJhLj7bducZHaiwQACgYKAYESARISFQHGX2MiHrHcCG6IYzc2Q8AMxhSWQRoVAUF8yKporACGevaSLGxG0x-kc7eK0076",
    "S": "billing-ui-v3=0vm8rTIKpRDgpj11CvWYsnbaukUu_MAb:billing-ui-v3-efe=0vm8rTIKpRDgpj11CvWYsnbaukUu_MAb",
    "__Secure-1PSIDTS": "sidts-CjIBjplskOOHqRfyeORGL_g5u6tvigMJhFEjFbyIAhmg24CQPbQ3qHD21qEPeb1JXbxFtRAA",
    "__Secure-3PSIDTS": "sidts-CjIBjplskOOHqRfyeORGL_g5u6tvigMJhFEjFbyIAhmg24CQPbQ3qHD21qEPeb1JXbxFtRAA",
    "_gid": "GA1.3.818868622.1747383919",
    "AEC": "AVcja2eMf9BdHdSI6msBqJeAVp-R4L4o8Rmu3XXm_W5l1BO2eVWdOnqpSQ",
    "NID": "524=IugAce36U5hOGbHVrJN9cvhbcvMpjAuOZqjknMEpZqOJaq0nNDgt982oOYI0b6E-WmouXLVDUJ8HlV_0-7WqUjPZbngaBhw-ivBnjQj5nROg-lIQgR-4TPVX-S8jh5x-35dJ3Pz6-p6FmtZ-Du-QWbuOYu_Um_wCnraox3Q_eNFZLOY7blny6N7ugGZ_2KNKUBqNCmRbtjWgZjVSY9RhbMHMpDPX0aoEpy0Y_0CYqgaN5YTjdbUpSxi4k_9XhLV1QLnc-DOKnp2FspA-uZ4WigZat0xtFqD1QCQwq07hwGWzs9FNkyvPTqzFmFECCvga8tQVeeNxdGtdtnCbOVFMdzC4pHRt8sYCWulBL34rj684kS4mGBw0rkAsAlmirbXELDgXl3mlDNhGn0ZnbY55osakQYQ8XYO-bd3oWrh9aP6JXTkfEfS6vpMMLR8e2ipJgsaDqAER-1MgJ5k8crUZHzp3L9lhZ7MlSa7KpRLcUd2AAQdk_e49b0nzJtFpQtHKM1c2f-VYoLZ2Q9sJvX8st72QjyR8lH0-IpL5_rZgIPbXZvSFCKNnGtDjS5ZrSq9hw4jGCukSvika9570EcNly73U7wvetHZxyc4Tp7-gbJ4y_SFqlE9wnhQuCfNWVKqJZusAvrYhmlZdiebuvaEpzzzcIGwl",
    "_gat": "1",
    "_ga": "GA1.3.147074646.1747383919",
    "_gat_marketingTracker": "1",
    "_ga_S4FJY0X3VX": "GS2.1.s1747389947$o2$g1$t1747391495$j0$l0$h0",
    "SIDCC": "AKEyXzVPv4EFGrL99WVum2u1VxILbdb9PJV8RzM45BJjmznESlKFS7tXsqx2zETmDGmO4V1D_g",
    "__Secure-1PSIDCC": "AKEyXzXG4BPiUFJQHAjknn5vMeHXtpVpe-_wAlQ2YEI8QTl_MBkOEtVNJGE2rt2JbJ0zyo-_y9M",
    "__Secure-3PSIDCC": "AKEyXzXyaVGBwLCZfaYVjzp-TkTmforptXDMAi7DrGIoER7vPnvjM0qNhrDEtM_cDXRMxsjVWTo"
}

payload_str = '''
{
  "dataRequest": [
    {
      "requestContext": {
        "reportContext": {
          "reportId": "5513a22b-6546-4435-94a7-b00d37cfeae1",
          "pageId": "p_bjphlvetcd",
          "mode": 1,
          "componentId": "cd-l02j96ggfd",
          "displayType": "simple-table"
        },
        "requestMode": 0
      },
      "datasetSpec": {
        "dataset": [
          {
            "datasourceId": "2fb856c7-6546-4fca-9203-1fb97a43095e",
            "revisionNumber": 0,
            "parameterOverrides": []
          }
        ],
        "queryFields": [
          {
            "name": "qt_5kfh1xxlfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "dataTransformation": {
              "sourceFieldName": "_1701523289_"
            }
          },
          {
            "name": "qt_uqew8xxlfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "dataTransformation": {
              "sourceFieldName": "_2577255_"
            }
          },
          {
            "name": "qt_05v7ayxlfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "dataTransformation": {
              "sourceFieldName": "_80888_"
            }
          },
          {
            "name": "qt_c1v6dyxlfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "dataTransformation": {
              "sourceFieldName": "_2100359414_"
            }
          }
        ],
        "sortData": [
          {
            "sortColumn": {
              "name": "qt_5kfh1xxlfd",
              "datasetNs": "d0",
              "tableNs": "t0",
              "dataTransformation": {
                "sourceFieldName": "_1701523289_"
              }
            },
            "sortDir": 0
          },
          {
            "sortColumn": {
              "name": "qt_c1v6dyxlfd",
              "datasetNs": "d0",
              "tableNs": "t0",
              "dataTransformation": {
                "sourceFieldName": "_2100359414_"
              }
            },
            "sortDir": 0
          }
        ],
        "includeRowsCount": true,
        "relatedDimensionMask": {
          "addDisplay": false,
          "addUniqueId": false,
          "addLatLong": false
        },
        "paginateInfo": {
          "startRow": 1,
          "rowsCount": 250
        },
        "dsFilterOverrides": [],
        "filters": [
          {
            "filterDefinition": {
              "filterExpression": {
                "include": true,
                "conceptType": 0,
                "concept": {
                  "ns": "t0",
                  "name": "qt_148q6sf1fd"
                },
                "filterConditionType": "EQ",
                "stringValues": [
                  "Miscellaneous registration appointment"
                ],
                "numberValues": [],
                "queryTimeTransformation": {
                  "dataTransformation": {
                    "sourceFieldName": "_1701523289_"
                  }
                }
              }
            },
            "dataSubsetNs": {
              "datasetNs": "d0",
              "tableNs": "t0",
              "contextNs": "c0"
            },
            "version": 3
          }
        ],
        "features": [],
        "dateRanges": [],
        "contextNsCount": 1,
        "dateRangeDimensions": [
          {
            "name": "qt_agjtemrmfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "dataTransformation": {
              "sourceFieldName": "_2100359414_"
            }
          }
        ],
        "calculatedField": [],
        "needGeocoding": false,
        "geoFieldMask": [],
        "multipleGeocodeFields": [],
        "timezone": "Australia/Sydney"
      },
      "role": "main",
      "retryHints": {
        "useClientControlledRetry": true,
        "isLastRetry": false,
        "retryCount": 0,
        "originalRequestId": "cd-l02j96ggfd_0_0"
      }
    },
    {
      "requestContext": {
        "reportContext": {
          "reportId": "5513a22b-6546-4435-94a7-b00d37cfeae1",
          "pageId": "p_bjphlvetcd",
          "mode": 1,
          "componentId": "cd-wvskf0xlfd",
          "displayType": "dimension-filter"
        },
        "requestMode": 7
      },
      "datasetSpec": {
        "dataset": [
          {
            "datasourceId": "2fb856c7-6546-4fca-9203-1fb97a43095e",
            "revisionNumber": 0,
            "parameterOverrides": []
          }
        ],
        "queryFields": [
          {
            "name": "qt_gwdeu1xlfd",
            "datasetNs": "d0",
            "tableNs": "t0",
            "resultTransformation": {
              "analyticalFunction": 0,
              "isRelativeToBase": false
            },
            "dataTransformation": {
              "sourceFieldName": "_2577255_"
            }
          }
        ],
        "sortData": [
          {
            "sortColumn": {
              "name": "qt_gwdeu1xlfd",
              "datasetNs": "d0",
              "tableNs": "t0",
              "dataTransformation": {
                "sourceFieldName": "_2577255_"
              }
            },
            "sortDir": 0
          }
        ],
        "includeRowsCount": true,
        "relatedDimensionMask": {
          "addDisplay": false,
          "addUniqueId": false,
          "addLatLong": false
        },
        "paginateInfo": {
          "startRow": 1,
          "rowsCount": 5001
        },
        "dsFilterOverrides": [],
        "filters": [],
        "features": [],
        "dateRanges": [],
        "contextNsCount": 1,
        "calculatedField": [],
        "needGeocoding": false,
        "geoFieldMask": [],
        "multipleGeocodeFields": [],
        "timezone": "Australia/Sydney"
      },
      "role": "main",
      "retryHints": {
        "useClientControlledRetry": true,
        "isLastRetry": false,
        "retryCount": 0,
        "originalRequestId": "cd-wvskf0xlfd_0_0"
      }
    }
  ]
}
'''

payload = json.loads(payload_str)

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_earliest_mildura_appointment(json_data):
    # column[1] là vị trí, column[3] là ngày
    dataset = json_data['dataResponse'][0]['dataSubset'][0]['dataset']['tableDataset']
    locations = dataset['column'][1]['stringColumn']['values']
    dates = dataset['column'][3]['dateColumn']['values']
    mildura_dates = [dates[i] for i, loc in enumerate(locations) if loc == "Mildura"]
    if not mildura_dates:
        return None
    return sorted(mildura_dates)[0]

def main():
    # Gửi request lấy JSON
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    data = response.text
    # Nếu có ký tự dư thừa đầu (ví dụ )]}' ), hãy loại bỏ
    if data.startswith(")]}'"):
        data = data[4:].lstrip()
    json_data = json.loads(data)

    # Kiểm tra ngày sớm nhất của Mildura
    earliest = get_earliest_mildura_appointment(json_data)
    if earliest is None:
        print("Không tìm thấy lịch hẹn Mildura.")
        return
    print(f"Lịch hẹn sớm nhất Mildura: {earliest}")
    if earliest < YOUR_DATE:
        msg = f"ĐÃ CÓ LỊCH HẸN MILDURA SỚM HƠN: {earliest}"
        send_telegram_message(msg)
        print("Đã gửi thông báo Telegram.")
    else:
        print("Chưa có lịch hẹn Mildura sớm hơn.")

if __name__ == '__main__':
    main()