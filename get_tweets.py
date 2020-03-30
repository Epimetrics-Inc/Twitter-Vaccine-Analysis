import json
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import seaborn as sns
import pickle
import time
import datetime

start_date = datetime.date(2017,11,28)
end_date = datetime.date(2018,11,29)
num_tweets_per_api_call = 500
max_calls_per_day = 7
term = "dengue"

delta = end_date - start_date
dates = []
for i in range(delta.days + 2):
    day = start_date + datetime.timedelta(days=i)
    dates.append(str(day))
dates = [(s, e) for s, e in zip(dates, dates[1:])]

creds = load_credentials(filename="twitter_keys.yaml",
                 yaml_key="search_tweets_api",
                 env_overwrite=False)

for s, e in dates:
    rule = gen_rule_payload(f"{term} place_country:PH", from_date=s, #UTC 2017-09-01 00:00
                            to_date=e,
                            results_per_call=499)
    rs = ResultStream(**creds, rule_payload=rule,
                      max_requests=6,
                      tweetify=True)
    i = 0
    t = list(rs.stream())
    print(f"{s}-{i}-{len(t)}")
    pickle.dump(t, open(f"data/tweet_{s}_{term}_{i}", "wb" ))
    time.sleep(1.5)


