# import cv2
# import numpy

# img1 = cv2.imread(r"C:\Users\HP\Desktop\blood.jpg")
# img2= cv2.imread(r"C:\Users\HP\Desktop\blood.jpg")

# cv2.imshow("input Image1", img1)
# cv2.imshow("input Image2", img2)

# img=numpy.concatenate((img1,img2),axis=1)
# cv2.imshow("Concatenated Image",img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import numpy
# img1=cv2.imread(r"C:\Users\HP\Desktop\blood.jpg")
# img2=cv2.imread(r"C:\Users\HP\Desktop\blood.jpg")
# img=numpy.concatenate((img1,img2),axis=1)
# cv2.imshow("Concatenated Images",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# import cv2
# img = cv2.imread(r"C:\Users\HP\Desktop\blood.jpg", cv2.IMREAD_GRAYSCALE)
# imagename = 'blood.jpg'
# cv2.imwrite(imagename, img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# import cv2
# import matplotlib
# img = cv2.imread(r"C:\Users\HP\Desktop\blood.jpg")
# cv2.imshow('Normal output',img)
# half_image=cv2.resize(img,(100,100),fx=0.1,fy=0.1)

# cv2.imshow("resized image",half_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# import cv2
#  # image=cv2.imread("C:\Users\HP\Desktop\image.jpg\image.jpg")
# image = cv2.imread(r"C:\\Users\\HP\\Desktop\\image.jpg")


# cv2.imshow('Original Image',image)
# gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('Grayscale Image',gray)
# blur = cv2.GaussianBlur(gray,(5,5),0)
# cv2.imshow('Blurred Image',blur)
# val1,threshold=cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
# contour,val2=cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# contour_length=len(contour)
# print(contour_length)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




import cv2

image = cv2.imread(r"C:\Users\HP\Desktop\image.jpg\image.jpg")


cv2.imshow('Original Image', image)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale Image', gray)


blur = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('Blurred Image', blur)
val1, threshold = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
cv2.imshow('Threshold Image', threshold)

contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_length = len(contours)
print(contour_length)
if(contour_length<50):
    print('o')
elif(50<=contour_length<=100):
    print('A')
elif(100<=contour_length<=150):
    print('B')
else:
    print('AB')
cv2.waitKey(0)
cv2.destroyAllWindows()





