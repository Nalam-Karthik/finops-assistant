"""
database/seed.py

WHY THIS FILE EXISTS:
Empty tables can't demonstrate anything. This inserts realistic dummy data
so you have something to actually query. random.seed(42) makes the data
reproducible.
"""
import random
from app.database.session import SessionLocal
from app.models import Department, Employee, Project, CloudService, Billing, Budget

random.seed(42)

def seed():
    db = SessionLocal()
    
    # 1. Departments
    dept_data = [
        ("Engineering", "ENG"), ("Data Science", "DS"), ("Marketing", "MKT"),
        ("Sales", "SLS"), ("Platform / DevOps", "PLAT"),
    ]
    departments = [Department(name=n, code=c) for n, c in dept_data]
    db.add_all(departments)
    db.commit()  # Commit NOW so departments get real IDs before employees use them as Foreign Keys
    
    # Create a quick lookup dictionary to easily find department IDs by their code
    dept_by_code = {d.code: d for d in departments}
    
    # 2. Employees
    employee_data = [
        ("Ravi Kumar", "ravi.kumar@company.com", "Engineering Manager", "ENG"),
        ("Ananya Rao", "ananya.rao@company.com", "Senior Engineer", "ENG"),
        ("Vikram Shah", "vikram.shah@company.com", "Backend Engineer", "ENG"),
        ("Priya Menon", "priya.menon@company.com", "Data Scientist", "DS"),
        ("Arjun Nair", "arjun.nair@company.com", "ML Engineer", "DS"),
        ("Divya Iyer", "divya.iyer@company.com", "Analytics Lead", "DS"),
        ("Karan Malhotra", "karan.malhotra@company.com", "Marketing Manager", "MKT"),
        ("Sneha Reddy", "sneha.reddy@company.com", "Growth Marketer", "MKT"),
        ("Aditya Verma", "aditya.verma@company.com", "Sales Ops Lead", "SLS"),
        ("Neha Kapoor", "neha.kapoor@company.com", "Account Executive", "SLS"),
        ("Rohan Desai", "rohan.desai@company.com", "Platform Engineer", "PLAT"),
        ("Ishita Gupta", "ishita.gupta@company.com", "DevOps Engineer", "PLAT"),
        ("Manish Joshi", "manish.joshi@company.com", "FinOps Analyst", "PLAT"),
    ]
    employees = [Employee(name=n, email=e, role=r, department_id=dept_by_code[c].id)
                 for n, e, r, c in employee_data]
    db.add_all(employees)
    db.commit()
    
    emp_by_name = {e.name: e for e in employees}
    
    # 3. Projects
    project_data = [
        ("checkout-service-prod", "ENG", "Ravi Kumar"),
        ("user-auth-platform", "ENG", "Ananya Rao"),
        ("payments-gateway", "ENG", "Vikram Shah"),
        ("recommendation-engine", "DS", "Priya Menon"),
        ("churn-prediction-pipeline", "DS", "Arjun Nair"),
        ("bi-reporting-warehouse", "DS", "Divya Iyer"),
        ("campaign-tracker", "MKT", "Karan Malhotra"),
        ("seo-analytics-tool", "MKT", "Sneha Reddy"),
        ("sales-crm-integration", "SLS", "Aditya Verma"),
        ("lead-scoring-service", "SLS", "Neha Kapoor"),
        ("log-aggregation-platform", "PLAT", "Rohan Desai"),
        ("ci-cd-infrastructure", "PLAT", "Ishita Gupta"),
    ]
    projects = [Project(name=n, department_id=dept_by_code[c].id, owner_id=emp_by_name[o].id)
                for n, c, o in project_data]
    db.add_all(projects)
    db.commit()
    
    # 4. Cloud Services
    service_data = [
        ("Compute Engine", "Compute"), ("Kubernetes Engine", "Compute"),
        ("Cloud Functions", "Compute"), ("Cloud Storage", "Storage"),
        ("BigQuery", "Analytics"), ("Cloud SQL", "Database"),
        ("Cloud Pub/Sub", "Messaging"), ("Cloud CDN", "Networking"),
    ]
    services = [CloudService(name=n, category=c) for n, c in service_data]
    db.add_all(services)
    db.commit()
    
    # 5. Billing & Budgets (The Fact Tables)
    cost_ranges = {
        "Compute": (400, 5000), "Storage": (50, 800), "Analytics": (200, 3500),
        "Database": (100, 1500), "Messaging": (20, 300), "Networking": (30, 400),
    }
    months = [(3, 2026), (4, 2026), (5, 2026), (6, 2026)]
    
    billing_rows = []
    budget_rows = []
    
    for project in projects:
        # Assign 3 to 5 random services to each project
        services_used = random.sample(services, k=random.randint(3, 5))
        
        # Base budget for the project
        base_budget = round(random.uniform(1500, 8000), 2)
        
        for month, year in months:
            # Create Budget row
            budget_rows.append(Budget(project_id=project.id, month=month, year=year,
                                       budgeted_amount=base_budget))
            
            # Create Billing rows for each service
            for service in services_used:
                low, high = cost_ranges[service.category]
                amount = round(random.uniform(low, high), 2)
                billing_rows.append(Billing(project_id=project.id, cloud_service_id=service.id,
                                             month=month, year=year, amount=amount))
                
    db.add_all(billing_rows)
    db.add_all(budget_rows)
    db.commit()
    
    print(f"Seeded: {len(departments)} departments, {len(employees)} employees, "
          f"{len(projects)} projects, {len(services)} cloud services, "
          f"{len(billing_rows)} billing rows, {len(budget_rows)} budget rows.")
    db.close()

if __name__ == "__main__":
    seed()