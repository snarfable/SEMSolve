def convert_mc_to_gmsh(mc_filename, msh_filename):
    with open(mc_filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Parse header: total nodes and total elements
    header = lines[0].split()
    num_nodes = int(header[0])
    num_elements = int(header[1])
    
    nodes = []
    elements = []
    
    # Extract Node Coordinates
    for i in range(1, num_nodes + 1):
        coords = lines[i].split()
        # Force 3D even if 2D input (add Z=0.0)
        x = coords[0]
        y = coords[1]
        z = coords[2] if len(coords) > 2 else "0.0"
        nodes.append((i, x, y, z))
        
    # Extract Element Connectivity
    for i in range(num_nodes + 1, num_nodes + 1 + num_elements):
        conn = lines[i].split()
        # Detect element type (3 nodes = Triangle, 4 nodes = Tetrahedron)
        if len(conn) == 3:
            el_type = 2  # 3-node triangle
        elif len(conn) == 4:
            el_type = 4  # 4-node tetrahedron
        else:
            raise ValueError(f"Unsupported element with {len(conn)} nodes.")
        
        # FETK MC uses 0-based or 1-based indexing depending on generation.
        # Gmsh strictly requires 1-based indexing.
        # If your MC nodes start at 0, uncomment the block below to shift them:
        # conn = [str(int(n) + 1) for n in conn]
        
        elements.append((i - num_nodes, el_type, conn))

    # Write to Gmsh MSH Format
    with open(msh_filename, 'w') as f:
        f.write("$MeshFormat\n2.2 0 8\n$EndMeshFormat\n")
        
        # Write Nodes section
        f.write("$Nodes\n")
        f.write(f"{num_nodes}\n")
        for node_id, x, y, z in nodes:
            f.write(f"{node_id} {x} {y} {z}\n")
        f.write("$EndNodes\n")
        
        # Write Elements section
        f.write("$Elements\n")
        f.write(f"{num_elements}\n")
        for el_id, el_type, conn in elements:
            # 2 tags (physical/elementary) set to default '1'
            conn_str = " ".join(conn)
            f.write(f"{el_id} {el_type} 2 1 1 {conn_str}\n")
        f.write("$EndElements\n")

    print(f"Successfully converted {mc_filename} to {msh_filename}")

# Usage Example:
# convert_mc_to_gmsh("my_mesh.mc", "my_mesh.msh")

