from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponseRedirect
import base64
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request,'text.html')
def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        un = request.POST['username']
        pw = request.POST['password']
        
        user = authenticate(request,username=un,password=pw)
        
        if(user is not None):
            return redirect('/profile')
        else:
            msg = 'Error in login. Invalid username/password'
            form = AuthenticationForm()
            return render(request,'login.html',{'form':form,'msg':msg})
    else:   
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
def register(request):
    if(request.user.is_authenticated):
        return redirect('/')
    
    if(request.method == "POST"):
        form=UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un =form.cleaned_data.get('username') 
            pw =form.cleaned_data.get('password1') 
            user = authenticate(username=un,password=pw)
            return redirect('/login')
        else:
            return render(request,'register.html',{'form':form})
    else:
        form=UserCreationForm()
        return render(request,'register.html',{'form':form})

def profile(request):
    return render(request,'profile.html')



# views.py
from django.shortcuts import render

def results(request):
    return render(request, 'results.html')



def profile(request):
    if(request.method=="Post"):
        if(request.FILES.get('abd')):
            img_name=request.FILES['abd'].read()
            encode=base64.b64encode(img_name).decode('utf-8')

            return render(request,'profile.html',{'img':img_url})
    else:
        return render(request,'profile.html')
    if(request.method=="Post"):
        if(request.FILES.get('abd')):
            img_name=request.FILES['abd']
            fs=FileSystemStorage
            filename=fs.save(img_name.name,img_name)
            img_url=fs.url(filename)
            return render(request,'profile.html',{'img':img_url})
        else:
            return render(request,'profile.html')




from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'


# import cv2

# # Replace 'path/to/your/image.png' with the correct path to your image
# image_path = ''
# image = cv2.imread(image_path)

# # Check if the image was loaded successfully
# if image is None:
#     raise ValueError(f"Error: Unable to load image at {image_path}")

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# # Apply a binary threshold to the image
# _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# # Find contours
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Print the number of contours
# print(f"Number of contours found: {len(contours)}")

# # Optionally, you can draw the contours on the original image for visualization
# cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# # Show the image with contours (optional)
# cv2.imshow("Contours", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

















# import cv2
# import numpy as np
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage

# def contour_length(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         # Get the uploaded image
#         uploaded_file = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(uploaded_file.name, uploaded_file)
#         img_path = fs.url(filename)

#         # Read the image using OpenCV
#         img = cv2.imread(uploaded_file.name)

#         # Convert the image to grayscale
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # Apply binary thresholding
#         _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

#         # Find contours
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         # Calculate the length (perimeter) of each contour
#         contour_lengths = []
#         for contour in contours:
#             length = cv2.arcLength(contour, True)  # True indicates the contour is closed
#             contour_lengths.append(length)

#         # Total length of all contours
#         total_length = sum(contour_lengths)

#         return render(request, 'profile.html', {
#             'img_url': img_path,
#             'contour_lengths': contour_lengths,
#             'total_length': total_length
#         })
    
#     return render(request, 'profile.html')


  





def profile(request):
    if request.method == "POST":  # Ensure the method is POST
        if request.FILES.get('abd'):  # Get the uploaded file with the correct key
            img_name = request.FILES['abd'].read()  # Correct file reference 'abd' instead of 'abc'
            encode = base64.b64encode(img_name).decode('utf-8')  # Base64 encode the image data
            
            # Decode the base64 string back into an image
            img_array = np.frombuffer(base64.b64decode(encode), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            
            # Histogram equalization for better contrast
            enhance_img = cv2.equalizeHist(blur_img)
            
            # Apply thresholding to the enhanced image
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Create a kernel for morphological transformations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            
            # Perform morphological opening and closing to clean up the image
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)


            hei,wid=bin_img.shape
            mid_wid=wid//3
            region_A=bin_img[0:mid_wid]
            region_B=bin_img[mid_wid:2*mid_wid]
            region_D=bin_img[2*mid_wid:]



            #calculate the default formula for our blood group that is aggulation
            def cal_agg(region):
                num_labels,labels,stats,var=cv2.connectedComponentsWithStats(region,connectivity=8)
                return num_labels-1
            num_region_A=cal_agg(region_A)
            num_region_B=cal_agg(region_B)
            num_region_D=cal_agg(region_D)
            print(num_region_A,num_region_B,num_region_D)

            
           #calculate the morphological bin_img into base64 img
            var,img=cv2.imencode('.jpg',bin_img)
            mor_img=base64.b64encode(img).decode('utf-8')
            mor_img_url=f"data:image/jpge;base64,{mor_img}"



            # Encode the processed binary image back into base64
            _, buffer = cv2.imencode('.jpg', bin_img)
            bin_img_encoded = base64.b64encode(buffer).decode('utf-8')
            
            # Correct base64 image URL format:
            bin_img_url = f"data:image/jpeg;base64,{bin_img_encoded}"
            
            # Return the image URL (base64 encoded) to be displayed in the template
            return render(request, 'profile.html', {'img': bin_img_url})
    else:
        return render(request, 'profile.html')




import numpy as np

# Create a binary matrix with a visual break between 255 and 0
def create_binary_matrix_with_visual_break(rows, cols):
    # Ensure the number of rows is sufficient for a break
    assert rows >= 3, "The number of rows must be at least 3 for a proper break."
    
    half_rows = rows // 2
    matrix = np.zeros((rows, cols), dtype=np.uint8)  # Initialize with zeros
    
    # Fill the top half with 255
    matrix[:half_rows, :] = 255
    
    # Bottom half remains as 0 (initialized to 0 by default)
    return matrix

# Generate a 10x10 binary matrix
rows, cols = 10, 10
binary_image = create_binary_matrix_with_visual_break(rows, cols)

# Print the binary matrix (full with a break)
print("Full Binary Matrix:")
for i, row in enumerate(binary_image):
    if i == rows // 2:  # Add a visual break
        print()  # Blank line for separation
    print(row)

print("\nBinary Matrix Preview (5x5):")
print(binary_image[:5, :5])

# Get unique values
unique_values = np.unique(binary_image)
print("\nUnique Values in Binary Matrix:")
print(unique_values)

















# import cv2
# import base64
# import numpy as np
# from django.shortcuts import render

# def profile(request):
#     if request.method == "POST":  # Ensure the method is POST
#         if request.FILES.get('abd'):  # Get the uploaded file with the correct key
#             img_name = request.FILES['abd'].read()  # Correct file reference 'abd'
#             encode = base64.b64encode(img_name).decode('utf-8')  # Base64 encode the image data
            
#             # Decode the base64 string back into an image
#             img_array = np.frombuffer(base64.b64decode(encode), np.uint8)
#             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
#             # Convert the image to grayscale
#             gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
#             # Apply Gaussian blur
#             blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            
#             # Histogram equalization for better contrast
#             enhance_img = cv2.equalizeHist(blur_img)
            
#             # Apply thresholding to the enhanced image
#             _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
#             # Create a kernel for morphological transformations
#             kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            
#             # Perform morphological opening and closing to clean up the image
#             bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
#             bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

#             # Split the binary image into three regions
#             height, width = bin_img.shape
#             mid_width = width // 3
#             region_A = bin_img[:, 0:mid_width]
#             region_B = bin_img[:, mid_width:2 * mid_width]
#             region_D = bin_img[:, 2 * mid_width:]

#             # Calculate the number of aggregations for each region
#             def calculate_aggregation(region):
#                 num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(region, connectivity=8)
#                 return num_labels - 1

#             num_region_A = calculate_aggregation(region_A)
#             num_region_B = calculate_aggregation(region_B)
#             num_region_D = calculate_aggregation(region_D)

#             # Determine Rh factor (positive or negative)
#             if num_region_D > 0:
#                 rh_factor = "Positive"
#             else:
#                 rh_factor = "Negative"

#             # Determine blood type based on region A and B
#             # if num_region_A > 0 and num_region_B == 0:
#             #     blood_type = "A"
#             # elif num_region_A == 0 and num_region_B > 0:
#             #     blood_type = "B"
#             # elif num_region_A == 0 and num_region_B > 0:
#             #     blood_type = "AB"
#             # elif num_region_A == 0 and num_region_B == 0:
#             #     blood_type = "0"
#             # else:
#             #     blood_type = "Unknown"


#             if num_region_A > 0 and num_region_B == 0:
#                blood_type = "A"
#             elif num_region_A == 0 and num_region_B > 0:
#                blood_type = "B"
#             elif num_region_A > 0 and num_region_B > 0:
#               blood_type = "AB"
#             elif num_region_A == 0 and num_region_B == 0:
#               blood_type = "O"
#             else:
#               blood_type = "Unknown"


#             # Combine blood type with Rh factor
#             full_blood_type = f"{blood_type} {rh_factor}"

#             # Print the blood type
#             print(f"Blood Type: {full_blood_type}")
#             print(f"Agglutination Regions: A={num_region_A}, B={num_region_B}, D={num_region_D}")

#             # Encode the processed binary image back into base64
#             _, buffer = cv2.imencode('.jpg', bin_img)
#             bin_img_encoded = base64.b64encode(buffer).decode('utf-8')
            
            # # Correct base64 image URL format:
            # bin_img_url = f"data:image/jpeg;base64,{bin_img_encoded}"
            
            # Return the result to the template
    #         return render(request, 'profile.html', {
    #             'img': bin_img_url,
    #             'blood_type': full_blood_type,
    #             'region_A': num_region_A,
    #             'region_B': num_region_B,
    #             'region_D': num_region_D
    #         })
    # else:
    #     return render(request, 'profile.html')
    














import cv2
import base64
import numpy as np
from django.shortcuts import render

def profile(request):
    if request.method == "POST":  # Ensure the method is POST
        if request.FILES.get('abd'):  # Get the uploaded file
            img_data = request.FILES['abd'].read()  # Read the file data
            encoded_img = base64.b64encode(img_data).decode('utf-8')  # Base64 encode
            img_array = np.frombuffer(base64.b64decode(encoded_img), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                return render(request, 'profile.html', {'error': 'Invalid image uploaded.'})

            # Preprocess the image
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            enhance_img = cv2.equalizeHist(blur_img)
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

            # Split into three regions
            height, width = bin_img.shape
            mid_width = width // 3
            region_A = bin_img[:, 0:mid_width]
            region_B = bin_img[:, mid_width:2 * mid_width]
            region_D = bin_img[:, 2 * mid_width:]

            # Calculate agglutination
            def calculate_aggregation(region):
                num_labels, _, _, _ = cv2.connectedComponentsWithStats(region, connectivity=8)
                return num_labels - 1

            num_region_A = calculate_aggregation(region_A)
            num_region_B = calculate_aggregation(region_B)
            num_region_D = calculate_aggregation(region_D)

            # Determine Rh factor
            rh_factor = "Positive" if num_region_D > 0 else "Negative"

            # Determine blood type
            if num_region_A > 0 and num_region_B == 0:
                blood_type = "A"
            elif num_region_A == 0 and num_region_B > 0:
                blood_type = "B"
            elif num_region_A > 0 and num_region_B > 0:
                blood_type = "AB"
            elif num_region_A == 0 and num_region_B == 0:
                blood_type = "O"
            else:
                blood_type = "Unknown"

            # Combine blood type and Rh factor
            full_blood_type = f"{blood_type}{'+' if rh_factor == 'Positive' else '-'}"

            # Encode the processed image
            _, buffer = cv2.imencode('.jpg', bin_img)
            bin_img_encoded = base64.b64encode(buffer).decode('utf-8')
            bin_img_url = f"data:image/jpeg;base64,{bin_img_encoded}"

            # Return results to the template
            return render(request, 'profile.html', {
                'img': bin_img_url,
                'blood_type': full_blood_type,
                'region_A': num_region_A,
                'region_B': num_region_B,
                'region_D': num_region_D
            })

    return render(request, 'profile.html')

























































































import cv2
import base64
import numpy as np
from django.shortcuts import render

def profile(request):
    if request.method == "POST" and request.FILES.get('abd'):
        try:
            # Read the uploaded file
            img_data = request.FILES['abd'].read()
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                return render(request, 'profile.html', {'error': 'Invalid image uploaded.'})

            print("Image loaded successfully.")

            # Store the original uploaded image as it is for display
            _, img_buffer = cv2.imencode('.jpg', img)  # Original image (not grayscale)
            img_encoded = base64.b64encode(img_buffer).decode('utf-8')
            img_url = f"data:image/jpeg;base64,{img_encoded}"

            # Convert to grayscale (black and white)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Preprocess for binary processing
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            enhance_img = cv2.equalizeHist(blur_img)
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

            print("Image processed successfully (grayscale and binary).")

            # Split into three regions for analysis
            height, width = bin_img.shape
            mid_width = width // 3
            region_A = bin_img[:, 0:mid_width]
            region_B = bin_img[:, mid_width:2 * mid_width]
            region_D = bin_img[:, 2 * mid_width:]

            # Calculate agglutination
            def calculate_aggregation(region):
                num_labels, _, _, _ = cv2.connectedComponentsWithStats(region, connectivity=8)
                return num_labels - 1

            num_region_A = calculate_aggregation(region_A)
            num_region_B = calculate_aggregation(region_B)
            num_region_D = calculate_aggregation(region_D)

            print(f"Region A: {num_region_A}, Region B: {num_region_B}, Region D: {num_region_D}")

            # Determine Rh factor
            rh_factor = "Positive" if num_region_D > 0 else "Negative"

            # Determine blood type
            if num_region_A > 10 and num_region_B <= 10:
                blood_type = "A"
            elif num_region_A <=10  and num_region_B > 10:
                blood_type = "B"
            elif num_region_A > 10 and num_region_B > 10:
                blood_type = "AB"
            elif num_region_A <= 10 and num_region_B <=10:
                blood_type = "O"
            else:
                blood_type = "Unknown"

            # Combine blood type and Rh factor
            full_blood_type = f"{blood_type}{'+' if rh_factor == 'Positive' else '-'}"

            print(f"Blood Type: {full_blood_type}")

            # Encode grayscale and binary images for rendering in template
            _, gray_buffer = cv2.imencode('.jpg', gray_img)
            gray_img_encoded = base64.b64encode(gray_buffer).decode('utf-8')
            gray_img_url = f"data:image/jpeg;base64,{gray_img_encoded}"

            _, bin_buffer = cv2.imencode('.jpg', bin_img)
            bin_img_encoded = base64.b64encode(bin_buffer).decode('utf-8')
            bin_img_url = f"data:image/jpeg;base64,{bin_img_encoded}"

            # Return both images and results to the template
            return render(request, 'profile.html', {
                'original_img': img_url,  # Display original image (not grayscale)
                'gray_img': gray_img_url,
                'bin_img': bin_img_url,
                'blood_type': full_blood_type,
                'region_A': num_region_A,
                'region_B': num_region_B,
                'region_D': num_region_D,
            })

        except Exception as e:
            return render(request, 'profile.html', {'error': f"Error processing image: {str(e)}"})

    return render(request, 'profile.html')















