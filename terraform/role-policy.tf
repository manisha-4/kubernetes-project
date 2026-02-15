# resource "aws_eks_access_entry" "github_deployer" {
#   cluster_name = "eks-test-cluster"
#   principal_arn = "arn:aws:iam::990751731740:role/eks-deploy-role"
# }

# resource "aws_eks_access_policy_association" "github_deployer_admin" {
#   cluster_name = data.aws_eks_cluster.eks_test.name
#   principal_arn = aws_eks_access_entry.github_deployer.principal_arn
#   policy_arn   = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

#   access_scope {
#     type = "cluster"
#   }
# }
