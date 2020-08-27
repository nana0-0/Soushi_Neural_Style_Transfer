from neural_style.stylize import stylize
from PIL import Image
import scipy
import numpy as np
import json

ITERATIONS = 1000

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def neural_style_transfer(filename,style_path):

    # default arguments
    CONTENT_WEIGHT = 5e0
    CONTENT_WEIGHT_BLEND = 1
    STYLE_WEIGHT = 5e2
    TV_WEIGHT = 1e2
    STYLE_LAYER_WEIGHT_EXP = 1
    LEARNING_RATE = 1e1
    BETA1 = 0.9
    BETA2 = 0.999
    EPSILON = 1e-08
    VGG_PATH = "./neural_style/imagenet-vgg-verydeep-19.mat"
    POOLING = "max"
    CONTENT_PATH = f"./uploads/{filename}"
    OUTPUT_PATH = "./output/"
    STYLE_PATH = style_path
    def imread(path):
        im = Image.open(path)
        im = im.convert("RGB")
        im.thumbnail((500,500))
        # img = scipy.misc.imread(path).astype(np.float)
        # if len(img.shape) == 2:
        #     # grayscale
        #     img = np.dstack((img, img, img))
        # elif img.shape[2] == 4:
        #     # PNG with alpha channel
        #     img = img[:, :, :3]
        img = np.array(im)
        print(img.shape)
        return img


    def imsave(path, img):
        img = np.clip(img, 0, 255).astype(np.uint8)
        Image.fromarray(img).save(path, quality=95)


    for iteration, image, loss_vals in stylize(
        network=VGG_PATH,
        initial=None,
        initial_noiseblend=1.0,
        content=imread(CONTENT_PATH),
        styles=[imread(STYLE_PATH)],
        preserve_colors=False,
        iterations=ITERATIONS,
        content_weight=CONTENT_WEIGHT,
        content_weight_blend=CONTENT_WEIGHT_BLEND,
        style_weight=STYLE_WEIGHT,
        style_layer_weight_exp=STYLE_LAYER_WEIGHT_EXP,
        style_blend_weights=[1.0 / len([imread(STYLE_PATH)]) for _ in [imread(STYLE_PATH)]],
        tv_weight=TV_WEIGHT,
        learning_rate=LEARNING_RATE,
        beta1=BETA1,
        beta2=BETA2,
        epsilon=EPSILON,
        pooling=POOLING,
        print_iterations=20,
        checkpoint_iterations=20,
    ):
        if image is not None:
            imsave(OUTPUT_PATH + f"{filename}.{iteration}.jpg", image)

            if loss_vals is not None:
                print("loss",loss_vals)

            with open(OUTPUT_PATH+f"{filename}.{iteration}.json","w") as loss_vals_file:
                loss_vals_file.write(json.dumps(loss_vals,cls=MyEncoder))