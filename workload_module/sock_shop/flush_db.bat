kubectl exec -n pema-sock-shop carts-db-6d7546f9f9-gqntw -- mongo data --eval "db.cart.remove({})"
kubectl exec -n pema-sock-shop carts-db-6d7546f9f9-gqntw -- mongo data --eval "db.item.remove({})"
kubectl exec -n pema-sock-shop orders-db-5bf887f4c-rz4bs -- mongo data --eval "db.customerOrder.remove({})"
