# ActionKit Event Merge

This Python 3 script copies all attendees and hosts from one ActionKit event to another, then cancels the source event, effectively merging two events.

## Setup

```
git clone git@github.com:MoveOnOrg/misc_scripts.git
cd misc-scripts/ak-event-merge
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```
To run: 

```
  python merge.py --FROM_EVENT <fromevent_ID> --TO_EVENT <toevent_ID> --SIGNUP_PAGE <event_campaign_signup_page_integer_ID> --AK_BASEURL https://act.moveon.org/ --AK_USER <youruser> --AK_PASS <yourpass>
```
Use [this query](https://redash.moveon.casa/queries/5745/source?p_fromevent_id=13161&p_toevent_id=18122#6668) to check the results.