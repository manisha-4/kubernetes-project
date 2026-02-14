

# Fetch cluster details
data "aws_eks_cluster" "eks_test" {
  name = "eks-test-cluster"
}

# Fetch cluster auth details
data "aws_eks_cluster_auth" "eks_test" {
  name = data.aws_eks_cluster.eks_test.name
}

# Example: Use cluster details
output "cluster_endpoint" {
  value = data.aws_eks_cluster.eks_test.endpoint
}

output "cluster_certificate_authority" {
  value = data.aws_eks_cluster.eks_test.certificate_authority[0].data
}

output "cluster_identity_oidc" {
  value = data.aws_eks_cluster.eks_test.identity[0].oidc[0].issuer
}
