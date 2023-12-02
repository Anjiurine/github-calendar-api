# -*- coding: UTF-8 -*-
import requests
import json
from http.server import BaseHTTPRequestHandler
import os

token = os.environ.get("GITHUB_TOKEN")

query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

def getdata(name):
    response = requests.post("https://api.github.com/graphql", json={"query": query, "variables": {"login": name}}, headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    contributions = calendar["totalContributions"]
    datalist = [{"date": day["date"], "count": day["contributionCount"]} for week in calendar["weeks"] for day in week["contributionDays"]]
    returndata = {
        "total": contributions,
        "contributions": [datalist[i:i + 7] for i in range(0, len(datalist), 7)]
    }
    return returndata

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
