# Usage Examples

## 1. Basic summary

```bash
terraform show -json plan.tfplan > plan.json
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json
```

Output:

```text
Terraform Plan Summary: 5 change(s)

  + 2 will be created:
    + aws_instance.web
    + aws_security_group.web

  ~ 2 will be updated:
    ~ aws_rds_cluster.main [engine, instance_class]

  - 1 will be destroyed:
    - aws_instance.old_web

  Resource type distribution:
    aws_instance: 2
    aws_security_group: 1
    aws_rds_cluster: 1

  WARNING: Destructive changes detected:
    - aws_instance.old_web
```

## 2. From stdin

```bash
terraform show -json plan.tfplan | python skills/terraform-plan-summarizer/scripts/summarize_plan.py -
```

## 3. JSON output

```bash
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json --json
```

## 4. CI: fail on destructive changes

```bash
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json --exit-code
echo $?
# 1 if any delete/recreate/force-new changes exist
```

## 5. Filter by action type

```bash
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json --filter delete
```
