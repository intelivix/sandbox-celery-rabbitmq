from decouple import config
import requests

COVERALLS_REPO_TOKEN = config('COVERALLS_REPO_TOKEN')
COVERALLS_REPO = config('COVERALLS_REPO')
COVERALLS_BRANCH = config('COVERALLS_BRANCH', default='master')
"""
{
    "created_at": "2018-12-17T22:30:33Z",
    "url": null,
    "commit_message": "Utilizando variaveis de ambiente.",
    "branch": "loafer",
    "committer_name": "Arthur Alvim",
    "committer_email": "afmalvim@gmail.com",
    "commit_sha": "d02ca5cf77f249fce62ae2d7cf28cc2560490ef5",
    "repo_name": "intelivix/sandbox-celery-rabbitmq",
    "badge_url": "https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_14.svg",
    "coverage_change": 13.7,
    "covered_percent": 13.7055837563452
}
"""


def call_coveralls(page=1):
    url = (f'https://coveralls.io/github/{COVERALLS_REPO}.json?'
           f'repo_token={COVERALLS_REPO_TOKEN}&page={page}')
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_builds_by_branch(response, branch=COVERALLS_BRANCH):
    return list(filter(lambda x: x.get('branch') == branch,
                       response.get('builds')))


def get_last_build(builds):
    print(builds)
    return builds[0]


if __name__ == '__main__':

    coveralls_ = call_coveralls()
    builds = get_builds_by_branch(coveralls_)

    if not builds:
        current_page = coveralls_.get('page')
        total_pages = coveralls_.get('pages')
        while current_page < total_pages or len(builds) == 0:
            current_page += 1
            coveralls_ = call_coveralls(current_page)
            current_page = coveralls_.get('page')
            builds = get_builds_by_branch(coveralls_)

    build = get_last_build(builds)
    print(build.get('covered_percent'))
