import osmnx as ox
from PIL import Image

if __name__ == "__main__":

    file_name = 'test'
    extension = '.jpg'
    file_path = file_name + extension
    # get graph frome center and distance
    G = ox.graph_from_point((37.8891505835, 23.4384444463), dist=500, network_type='all')
    ox.plot_graph(G, show=False, save=True, filepath=file_path)

    image = Image.open(file_path)
    image_resized_128 = image.resize((512, 512))

    file_path = file_name + '_resized_512' + extension
    image_resized_128.save(file_path)

    from PIL import Image
    #Read the two images
    network_image = Image.open(file_path)
    network_image.show()
    original_image_file_path = 'extracted-data\imagery\\athina, gr\Agricultural + Semi-natural areas + Wetlands\\athina_z17_s512_37.8891505835_23.4384444463_grid-i0_grid-j23.jpg'
    satellite_image = Image.open(original_image_file_path)
    satellite_image.show()
    #resize, first image
    # network_image = network_image.resize((426, 240))
    network_image_size = network_image.size
    satellite_image_size = satellite_image.size
    merged_image = Image.new('RGB',(network_image_size[0], network_image_size[1]), (250,250,250))
    merged_image.paste(network_image,(0,0))
    merged_image.paste(satellite_image,(0,0))
    final_file_path = "extracted-data/merged/test_merged_image.jpg"
    image_type = "JPEG"
    merged_image.save(final_file_path, image_type)
    merged_image.show()