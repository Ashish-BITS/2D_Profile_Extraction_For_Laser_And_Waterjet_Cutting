import cv2
import numpy as np

f = open("result_corner.txt", "w")


img = cv2.imread('resources/Pics_Redrawn/4.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for i in contours:
    img = cv2.imread('resources/Pics_Redrawn/4.jpg')
    size = cv2.contourArea(i)
    rect = cv2.minAreaRect(i)
    if size <10000:
        gray = np.float32(gray)
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.fillPoly(mask, [i], (255,255,255))
        dst = cv2.cornerHarris(mask,5,3,0.04)
        ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
        if len(corners) >= 4:
            if rect[2] == 0 and len(corners) == 5:
                x,y,w,h = cv2.boundingRect(i)
                if w == h or w == h +3: #Just for the sake of example
                    shape = 'Square corners: '
                    print('Square corners: ')
                    for i in range(1, len(corners)):
                        print(corners[i])
                        coord = str(corners[i])
                    #f.write("\n")
                else:
                    print('Rectangle corners: ')
                    shape = 'Rectangle corners: '
                    for i in range(1, len(corners)):
                        print(corners[i])
                        coord = str(corners[i])
                    #f.write("\n")
            elif len(corners) == 5 and rect[2] != 0:
                print('Rombus corners: ')
                shape = 'Rombus corners: '
                for i in range(1, len(corners)):
                    print(corners[i])
                    coord = str(corners[i])
                #f.write("\n")
            elif len(corners) == 4:
                print('Triangle corners: ')
                shape = 'Triangle corners: '
                for i in range(1, len(corners)):
                    print(corners[i])
                    coord = str(corners[i])
                #f.write("\n")
            elif len(corners) == 6:
                print('Pentagon corners: ')
                shape = 'Pentagon corners: '
                for i in range(1, len(corners)):
                    print(corners[i])
                    coord = str(corners[i])
                #f.write("\n")
        else: continue
        img[dst>0.1*dst.max()]=[0,0,255]
        cv2.imshow('image', img)
        k = cv2.waitKey(0)
        if k == ord('s'):
            f.write(shape)
            f.write(coord)
            f.write("\n")
        cv2.destroyAllWindows


f.close()