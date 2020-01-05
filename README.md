
There is also another way. You can directly use the python executable from environment in ExecStart like this:

ExecStart=/path/to/conda/envs/my_env_name/bin/python /path/to/executable
For my CentOS server where I'm using miniconda the path is:

ExecStart=/root/miniconda3/envs/test_env/bin/python3 /root/test.py


https://unix.stackexchange.com/questions/478999/how-can-i-make-an-executable-run-as-a-service



with open('newdata.csv') as fp:
    content = fp.read()

response = requests.post(
    '{}/files/newdata.csv'.format(API_URL), headers=headers, data=content
)

response.status_code