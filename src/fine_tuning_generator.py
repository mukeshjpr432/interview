"""
Fine-tuning Data Generator
Creates training data for Bedrock model customization
Generates interview Q&A pairs for specific IT categories
"""

import json
import boto3
from typing import List, Dict, Any
from datetime import datetime


class FineTuningDataGenerator:
    """Generates training data for fine-tuning Bedrock models"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name='us-east-1')
        self.bucket = 'interview-coach-training-data'
        
    def generate_python_backend_training_data(self) -> List[Dict[str, str]]:
        """Generate training data for Python Backend Engineer interviews"""
        
        training_pairs = [
            {
                "system": "You are Sophia, an expert Python backend interview coach.",
                "user": "What is the difference between synchronous and asynchronous programming?",
                "assistant": "Great question! Synchronous programming is blocking - operations execute one after another. Asynchronous allows operations to run independently. In Python, async/await enables non-blocking I/O, crucial for web servers handling multiple requests. For example, with FastAPI and async endpoints, you can handle thousands of concurrent requests without blocking."
            },
            {
                "system": "You are Sophia, an expert Python backend interview coach.",
                "user": "How would you design a REST API for a social media platform?",
                "assistant": "I'd structure it around core resources: users, posts, comments. Key endpoints include GET /users/{id}, POST /posts, GET /posts/{id}/comments. I'd use FastAPI for performance, SQLAlchemy ORM for database abstraction. For scale, I'd implement pagination, caching with Redis, rate limiting, and consider microservices for notifications. Authentication via JWT tokens, with proper authorization checks."
            },
            {
                "system": "You are Sophia, an expert Python backend interview coach.",
                "user": "Tell me about database indexing and when to use it.",
                "assistant": "Indexing speeds up query performance but adds overhead to writes. I'd create indexes on frequently queried columns - like user_id in a posts table. Use composite indexes for queries filtering on multiple columns. Monitor slow queries using EXPLAIN ANALYZE. Avoid over-indexing as it slows inserts/updates. For very large tables, consider partitioning alongside indexes."
            },
            {
                "system": "You are Sophia, an expert Python backend interview coach.",
                "user": "How do you handle database migrations in production?",
                "assistant": "I use tools like Alembic with SQLAlchemy. Key practices: write reversible migrations, test on production-like data, deploy during low-traffic windows, have rollback plans. For zero-downtime: add column first, then application code, then remove old code. Always backup before migrations. Use blue-green deployment or canary releases."
            },
            {
                "system": "You are Sophia, an expert Python backend interview coach.",
                "user": "Describe your approach to API authentication and security.",
                "assistant": "I use JWT tokens for stateless authentication - clients include tokens in Authorization headers. Never store sensitive data in tokens. I implement refresh tokens with short expiry. For authorization, use role-based access control (RBAC). Always use HTTPS, validate input, use parameterized queries against SQL injection. Implement rate limiting, CORS properly, and log security events."
            }
        ]
        
        return training_pairs
    
    def generate_react_frontend_training_data(self) -> List[Dict[str, str]]:
        """Generate training data for React Frontend Engineer interviews"""
        
        training_pairs = [
            {
                "system": "You are Sophia, an expert React interview coach.",
                "user": "Explain React hooks and why they were introduced.",
                "assistant": "Hooks allow using state and effects in functional components. Before hooks, you needed class components for state management. Hooks like useState for state, useEffect for side effects, and useContext for prop drilling. They make code more reusable and easier to test. Custom hooks let you extract logic. They were introduced to address code reuse and complexity issues in class components."
            },
            {
                "system": "You are Sophia, an expert React interview coach.",
                "user": "How would you optimize a slow React component?",
                "assistant": "First, identify bottlenecks using React DevTools. Common optimizations: use React.memo for preventing unnecessary re-renders, useMemo for expensive calculations, useCallback for stable function references. Check if parent re-renders are causing child re-renders. Code splitting with React.lazy for route-based splitting. Use virtualization for long lists. Profile with Chrome DevTools performance tab."
            },
            {
                "system": "You are Sophia, an expert React interview coach.",
                "user": "What's your approach to state management in large applications?",
                "assistant": "For small apps, Context API suffices. For complex state, I'd use Redux or Zustand. Redux provides predictable state, time-travel debugging, middleware support. For simpler needs, Zustand is lighter. Architecture matters: normalize state shape, keep selectors memoized, use Redux Thunk or Saga for async. Consider MobX if you prefer reactive programming. Most importantly, keep state close to where it's used."
            },
            {
                "system": "You are Sophia, an expert React interview coach.",
                "user": "How do you handle testing in React applications?",
                "assistant": "I use Jest for unit tests and React Testing Library for component tests. Test behavior, not implementation. Use userEvent for simulations. Mock API calls with MSW (Mock Service Worker). For integration tests, test user workflows. E2E tests with Cypress for critical paths. Aim for high coverage on critical components. Use snapshot tests sparingly - they can be brittle."
            }
        ]
        
        return training_pairs
    
    def generate_devops_training_data(self) -> List[Dict[str, str]]:
        """Generate training data for DevOps Engineer interviews"""
        
        training_pairs = [
            {
                "system": "You are Sophia, an expert DevOps interview coach.",
                "user": "How would you design a CI/CD pipeline for microservices?",
                "assistant": "I'd use a multi-stage pipeline: build, test, security scan, staging deploy, production deploy. Each service has its own pipeline triggered on code push. Build Docker images, scan for vulnerabilities, run tests. Deploy to staging for integration testing. Use blue-green or canary deployments for production. Implement rollback capabilities. Monitor deployment health with dashboards."
            },
            {
                "system": "You are Sophia, an expert DevOps interview coach.",
                "user": "Explain your Kubernetes deployment strategy.",
                "assistant": "I use Helm charts for templating Kubernetes manifests. Deployments with rolling updates for zero-downtime. Health checks: liveness and readiness probes. Resource limits to prevent resource exhaustion. StatefulSets for databases, Daemonsets for monitoring agents. Use namespaces for isolation. RBAC for security. Service mesh like Istio for advanced traffic management. Monitor with Prometheus and Grafana."
            },
            {
                "system": "You are Sophia, an expert DevOps interview coach.",
                "user": "How do you handle secrets management in production?",
                "assistant": "Never commit secrets to git. Use dedicated tools: AWS Secrets Manager, HashiCorp Vault, or Kubernetes Secrets with encryption. Rotate secrets regularly. Use short-lived credentials. Implement least privilege access. Audit secret access. For Kubernetes, enable encryption at rest. Integrate secret management in CI/CD pipelines. Use environment variables for different environments."
            }
        ]
        
        return training_pairs
    
    def generate_data_scientist_training_data(self) -> List[Dict[str, str]]:
        """Generate training data for Data Scientist interviews"""
        
        training_pairs = [
            {
                "system": "You are Sophia, an expert Data Science interview coach.",
                "user": "Explain the bias-variance tradeoff and how to handle overfitting.",
                "assistant": "Bias is error from overly simple models, variance from overly complex ones. High bias = underfitting, high variance = overfitting. Combat overfitting with: regularization (L1/L2), cross-validation, early stopping, dropout for neural networks. Use training/validation curves to diagnose. Collect more data if possible. Feature selection reduces complexity. Ensemble methods (random forest, boosting) reduce variance naturally."
            },
            {
                "system": "You are Sophia, an expert Data Science interview coach.",
                "user": "Walk me through your approach to handling imbalanced datasets.",
                "assistant": "First, use appropriate metrics: F1-score, precision-recall curves, ROC-AUC instead of accuracy. Techniques: resampling (oversampling minority, undersampling majority), SMOTE for synthetic samples, class weights in loss function, threshold adjustment. Try different algorithms - tree-based models handle imbalance better. Stratified cross-validation ensures consistent class distribution. Cost-sensitive learning penalizes minority class errors more."
            },
            {
                "system": "You are Sophia, an expert Data Science interview coach.",
                "user": "How do you approach feature engineering?",
                "assistant": "Understand domain first. Create features from existing ones: polynomial features, interactions, binning continuous variables. Handle missing values thoughtfully. Scale/normalize appropriately. Remove correlated features. Domain expertise matters - sometimes simple engineered features outperform complex ones. Use techniques like PCA for dimensionality reduction. Validate feature importance using models or statistical tests."
            }
        ]
        
        return training_pairs
    
    def create_jsonl_training_file(
        self,
        training_pairs: List[Dict[str, str]],
        category: str
    ) -> str:
        """
        Convert training pairs to JSONL format for Bedrock fine-tuning
        
        Args:
            training_pairs: List of training examples
            category: Category name (e.g., 'python_backend')
            
        Returns:
            S3 URI of uploaded training file
        """
        
        # Format for Claude fine-tuning
        jsonl_content = ""
        for pair in training_pairs:
            formatted = {
                "custom_system_prompt": pair["system"],
                "messages": [
                    {"role": "user", "content": pair["user"]},
                    {"role": "assistant", "content": pair["assistant"]}
                ]
            }
            jsonl_content += json.dumps(formatted) + "\n"
        
        # Save to S3
        filename = f"fine-tuning-data/{category}-training-{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=filename,
                Body=jsonl_content,
                ContentType='application/x-ndjson'
            )
            
            s3_uri = f"s3://{self.bucket}/{filename}"
            print(f"Training data uploaded: {s3_uri}")
            return s3_uri
            
        except Exception as e:
            print(f"Error uploading training data: {str(e)}")
            raise
    
    def generate_all_training_data(self):
        """Generate and upload training data for all categories"""
        
        categories = {
            'python_backend': self.generate_python_backend_training_data(),
            'react_frontend': self.generate_react_frontend_training_data(),
            'devops': self.generate_devops_training_data(),
            'data_scientist': self.generate_data_scientist_training_data()
        }
        
        results = {}
        for category, training_pairs in categories.items():
            s3_uri = self.create_jsonl_training_file(training_pairs, category)
            results[category] = {
                'uri': s3_uri,
                'samples': len(training_pairs),
                'status': 'uploaded'
            }
        
        return results
