import codeforces_api

api_key = '0db6f7b63f2f8b39517082a3a9b3aab9a095a5c5'
secret = 'fd171083d1089111512c117670e60cbf6ac3853e'
cf_api = codeforces_api.CodeforcesApi(api_key, secret)  # Authorized access to api.

parser = codeforces_api.CodeforcesParser()  # Create parser.

parser.problem_tags = ['Сортировки']

problem = cf_api.problemset_problems()
for problem in problem['problems']:
    if problem.tags.count('sortings') and problem.rating is not None and problem.rating < 1000:
        print(problem.name + " " + str(problem.rating) + " " + str(problem.tags))