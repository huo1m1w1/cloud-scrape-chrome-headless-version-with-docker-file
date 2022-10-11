# Introduction:

A web scraper application collects opensea.io NFTs' ranking information and corresponding images. Save NFT information as a table in AWS RDS postgreSQL database, and send images to AWS S3

# Instructions/prerequisit: 


Create an AWS account,  a key pair named 'lt-key', and a role with s3 full access named 's3-admin'.

AWS infrastructure setting: AWS RDS PostgreSQL database with name of "cloud-scraper" and S3 bucket with name of "cloud-scraper".

Login to AWS cloudformation, create a stack with template.yml, that's it.


# Alternative way:
Use github action, choose deploy to ecs
Or run ci/cd on WAS codebuild with buildspec.yml 





...........................................................
...........................................................

# Contact
Michael Mingwang Huo - https://www.linkedin.com/in/mingwang-huo-5b7a3548/ - huomingwang@hotmail.com

Project Link: https://github.com/huo1m1w1/cloud-scrape-chrome-headless-version-with-docker-file

Acknowledgments
  Thank you very much to Blair for his support and code review!
