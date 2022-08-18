>I've changed a bit task: function filtering out data that have updates count less that 2

To run this code locally you have to be sure:
- you've installed serverless on your machine
- you've created virtual environment via **virtualenv env**
- you've installed all requirements via **pip install -r requirements.txt**

To test function locally tun this command:
> serverless invoke local -f total_update --data '{"articles": ["Batman", "Washington", "Marvel", "Bounty", "Ukraine", "War", "Nuclear War", "proficient", "Noob"]}'

<h1>Test Plan:</h1>
<ol>
<li>check if the data actually parsed from the last month</li>
<li>check if there will be an empty updates for previous month</li>
<li>check correctness of filtered out data</li>
<li>check timeouts exceptions and possible behave on different exceptions</li>
</ol>

<h1>Possible optimization</h1>
<ol>maybe provide a faster obtaining result from wiki and following preparing data for processing</ol>

