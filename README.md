# COMP90024 Assignment 2 - Team 20
# An Exploration of Liveability in Melbourne

## Description
Melbourne is one of the main cities in Australia which has repeatedly appeared in kinds of
lists of most livable cities around the world, and the group assignment is dedicated to exploring
Melbourne’s livability. We selected two different topics, house price and income, in Melbourne
and compared with the same theme of Sydney city from collected tweets expressing emotions in
a positive rate.

The overall software systems are built on a multi-node of virtual machines through Melbourne
Research Cloud with Ansible and OpenStack, and harvesting tweets from the Twitter APIs.
Our group also download house price and income data from the AURIN platform and associated
CouchDB database with the AURIN data and preprocessed Twitter data. After presenting the
analysis and visualization of the data from database, we demonstrate the plots and the results
on the front-end web application.

At the end, all the could lead us to a conclusion that the livability of Melbourne and Sydney is
basically similar, and there is no obvious difference could be seen from the analytical diagrams.
However, judging from the positive rate of emotion in tweets, Melbourne still performs a little
better compared to Sydney and we could say that it is a livable city.
## Links
**Web Application Link** :
http://172.26.131.132:3000 (requires connection through Unimelb VPN)

**YouTube Demonstration Link** :
- Ansible Deployment: https://youtu.be/zxmNIVBY1gQ
- Web Page: https://youtu.be/MjdD0YRZgrk

## Collective Team Details (Member's Name/Student ID/Location)
- Cenxi Si 1052447 China
- Yipei Liu 1067990 China
- Jingdan Zhang 1054101 China
- Chengyan Dai 1054219 Melbourne
- Ruimin Sun 1052182 China

## Project Structure
- Ansible: source code for system deployment
- data: necessary data sets
- Twitter_harvester: source code for twitter harvester
- Web: source code for web application
- Twitter_Aurin_analysis.py: python file for data analysis
