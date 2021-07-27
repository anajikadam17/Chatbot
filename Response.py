



def textResponce(res):
    text = {"Text":res}
    message={"payload": [ text ] }
    return message
    
def buttonsResponce(res):
    text = {"Text":res}
    button = {"Buttons": [
                  {
                      "title": "great",
                      "payload": "great"
                  },
                  {
                      "title": "super sad",
                      "payload": "super sad"
                  }
              ]}
    message={"payload": [text,button] }
    return message
    
def imageResponce(res, tag):
    text = {"Text":res}
    image1 = "static/Img/nonveg.jpg"
    if tag=="vegMenu":
        # image1 = "https://i.imgur.com/nGF1K8f.jpg"
        image1 = "static/Img/veg.jpg"
    image = {"Image":image1}
    message={"payload": [ text, image ] }
    return message

def SampleimageResponce():
    text="Here is something to cheer you up 😉"
    image="https://i.imgur.com/nGF1K8f.jpg"
    message={"payload": [ text,image ] }
    return message