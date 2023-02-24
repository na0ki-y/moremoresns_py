from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image
import time
#https://huggingface.co/nlpconnect/vit-gpt2-image-captioning

def init_img2text():
    obj_img2text={}
    obj_img2text["model"] = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    obj_img2text["feature_extractor"] = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    obj_img2text["tokenizer"] = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    obj_img2text["device"] = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    obj_img2text["model"].to(obj_img2text["device"])
    obj_img2text["gen_kwargs"] = {"max_length": 16, "num_beams": 4}
    print("end init img2text")
    return obj_img2text
def predict_step(image_paths,obj_img2text):
  images = []
  for image_path in image_paths:
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = obj_img2text["feature_extractor"](images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(obj_img2text["device"])

  output_ids = obj_img2text["model"].generate(pixel_values, **obj_img2text["gen_kwargs"])

  preds = obj_img2text["tokenizer"].batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  return preds

def pred_one_img2text(img_path,obj_img2text):
  start = time.time()
  preds=predict_step([img_path],obj_img2text)#img_pathの配列にして渡す
  time_img2text=time.time()-start
  return {"pred_text":preds[0],"time_img2text":time_img2text}
if __name__=="__main__":
    obj_img2text=init_img2text()
    print(obj_img2text)
    preds=predict_step(['./tmp/img0.png'],obj_img2text) # ['a woman in a hospital bed with a woman in a hospital bed']
    print(preds)
    dic=pred_one_img2text('./tmp/img0.png',obj_img2text)
    print(dic)