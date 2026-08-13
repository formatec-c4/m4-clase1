from pathlib import Path

from diagrams import Cluster, Diagram, Edge, Node
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.rbac import RB, Role, User


OUTPUT = Path(__file__).with_name("rbac-lab")

with Diagram(
    "Cómo decide Kubernetes RBAC",
    filename=str(OUTPUT),
    show=False,
    outformat="png",
    direction="LR",
    graph_attr={
        "bgcolor": "white",
        "fontname": "Arial Bold",
        "fontsize": "20",
        "pad": "0.45",
        "ranksep": "0.8",
        "nodesep": "0.55",
        "splines": "ortho",
    },
    node_attr={"fontname": "Arial", "fontsize": "11"},
    edge_attr={"fontname": "Arial", "fontsize": "10", "color": "#137333"},
):
    identity = User("1. Identidad y grupo\nuser-2 · app-support")
    api = APIServer("2. API Server\nrecibe la solicitud")
    binding = RB("3. RoleBinding\nencuentra el Role")
    role = Role("4. Role\ncompara sus reglas")

    identity >> Edge(label="acción solicitada") >> api
    api >> Edge(label="consulta RBAC") >> binding >> role

    with Cluster("5. Decisión"):
        allowed = Node(
            "PERMITIDO\nla regla coincide",
            shape="box",
            style="rounded,filled",
            fillcolor="#e6f4ea",
            color="#188038",
        )
        forbidden = Node(
            "FORBIDDEN\nninguna regla coincide",
            shape="box",
            style="rounded,filled",
            fillcolor="#fce8e6",
            color="#c5221f",
        )

    role >> Edge(label="verbo + recurso + namespace", color="#188038") >> allowed
    role >> Edge(label="sin coincidencia", color="#c5221f") >> forbidden
