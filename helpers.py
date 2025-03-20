import uuid
def save_graph(graph):
    try:
        # Generate a random filename
        import os

        # Ensure the images directory exists
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        
        # Generate a random filename
        random_filename = os.path.join(images_dir, str(uuid.uuid4()) + ".png")
        
        # Save the image as a file
        with open(random_filename, "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
   
    except Exception:
        # This requires some extra dependencies and is optional
        pass