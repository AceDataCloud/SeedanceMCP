set -eu
. ./deploy/oauth-state.sh
cat deploy/production/deployment.yaml | sed 's/\${TAG}/'"$BUILD_NUMBER"'/g' | kubectl apply -f -
mark_oauth_key_initialized
kubectl apply -f deploy/production/service.yaml || true
kubectl apply -f deploy/production/ingress.yaml || true
