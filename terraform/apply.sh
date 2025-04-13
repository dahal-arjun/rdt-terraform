#!bin/bash
rm data_integration.zip
zip -r data_integration.zip data_integration/

#check if terraform is initialized
if [ ! -d ".terraform" ]; then
  terraform init
fi
terraform plan -out plan.out
#check if plan is valid
if [ $? -ne 0 ]; then
  echo "Plan is not valid"
  exit 1
else
  terraform apply -lock=false plan.out
fi

