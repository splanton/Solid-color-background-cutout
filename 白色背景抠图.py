from os import walk
from PIL import Image
 
def cut(root,filename):
    img = Image.open(root+'\\'+filename)
    img = img.convert("RGBA")
 
    pixdata = img.load()
    #先把外面一圈的白色像素扣掉，上下左右指要留下区域的上下左右边界
    left,upper,right,lower = 0,0,0,0
    #四次遍历图片，确定上下左右边界
    flag = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if not pixdata[x,y] == (255,255,255,255):
                left = x
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if not pixdata[x,y] == (255,255,255,255):
                upper = y
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for x in range(img.size[0]-1,-1,-1):
        for y in range(img.size[1]):
            if not pixdata[x,y] == (255,255,255,255):
                right = x
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for y in range(img.size[1]-1,-1,-1):
        for x in range(img.size[0]):
            if not pixdata[x,y] == (255,255,255,255):
                lower = y
                flag = 1
                break
        if flag == 1 :
            break
    #边界确定了，抠出来，再刷新一下pixdata
    img = img.crop((left,upper,right,lower))
    pixdata = img.load()

    #再把白色的像素抠成透明的，route是一个二维列表，分别对应每一个像素，
    #route[x][y] = 1说明这个像素是白色，而且有一条到达图片边界的路径，而且这条路径上全是白色像素
    #就是说这个像素是白的，而且不是不是图片边缘内部的像素，像是眼睛的眼白这种，这样的像素就要抠成透明的

    #建立route，指定初值全是0
    route = list()
    for x in range(img.size[0]):
        route.append([0])
        for y in range(img.size[1]):
            route[x].append([0])
    
    #再确定哪些像素要抠掉，原理是白色的，最边上的像素肯定要扣掉，就把那个像素的route改成1，
    #然后不是最边上的，白色的，而且它上下左右至少有一个像素要扣掉，那这个像素也得抠掉
    #这样子抠图就是由图片最外面一圈向内一圈圈地确定哪像像素要扣掉，图片内部的白色色块的边界因为周围至少有一个像素不是白色，就不会被扣掉，
    #白色色块的内部因为边界的像素都不会被抠掉，而扫描像素又是一圈一圈向内扫描，所以也不会被扣掉
    #但是一圈一圈地扫描像素代码写起来很麻烦，就改成从左到右，同时从上到下扫描一遍，再从上到下，从左到右扫描一遍，再从右到左、从上到下一遍，从下到上、从左到右一遍
    #上面那样再扫描一遍，和从外圈到内圈效果一样

    for i in range(2):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if (x==0 or y==0 or x==img.size[0]-1 or y==img.size[1]-1) and pixdata[x, y] == (255, 255, 255, 255):
                    route[x][y] = 1
                elif ((not x==0) and (not y==0) and (not x==img.size[0]-1) and (not y==img.size[1]-1)) and pixdata[x, y] == (255, 255, 255, 255) and (route[x-1][y] == 1 or route[x][y-1] == 1 or route[x+1][y] == 1 or route[x][y+1] == 1):
                    route[x][y] = 1

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if (x==0 or y==0 or x==img.size[0]-1 or y==img.size[1]-1) and pixdata[x, y] == (255, 255, 255, 255):
                    route[x][y] = 1
                elif ((not x==0) and (not y==0) and (not x==img.size[0]-1) and (not y==img.size[1]-1)) and pixdata[x, y] == (255, 255, 255, 255) and (route[x-1][y] == 1 or route[x][y-1] == 1 or route[x+1][y] == 1 or route[x][y+1] == 1):
                    route[x][y] = 1

        for x in range(img.size[0]-1,-1,-1):
            for y in range(img.size[1]):
                if (x==0 or y==0 or x==img.size[0]-1 or y==img.size[1]-1) and pixdata[x, y] == (255, 255, 255, 255):
                    route[x][y] = 1
                elif ((not x==0) and (not y==0) and (not x==img.size[0]-1) and (not y==img.size[1]-1)) and pixdata[x, y] == (255, 255, 255, 255) and (route[x-1][y] == 1 or route[x][y-1] == 1 or route[x+1][y] == 1 or route[x][y+1] == 1):
                    route[x][y] = 1

        for y in range(img.size[1]-1,-1,-1):
            for x in range(img.size[0]):
                if (x==0 or y==0 or x==img.size[0]-1 or y==img.size[1]-1) and pixdata[x, y] == (255, 255, 255, 255):
                    route[x][y] = 1
                elif ((not x==0) and (not y==0) and (not x==img.size[0]-1) and (not y==img.size[1]-1)) and pixdata[x, y] == (255, 255, 255, 255) and (route[x-1][y] == 1 or route[x][y-1] == 1 or route[x+1][y] == 1 or route[x][y+1] == 1):
                    route[x][y] = 1

    #哪些像素要抠确定好了，抠
    for x in range(img.size[0]):
        for y in range(img.size[1]):
          if route[x][y] == 1:
                pixdata[x, y] = (0, 0, 0, 0)

    #最后就是这个算法只是实现边缘检测，但只能检测到算法认为的边缘，比如一条丝带围了一圈，在人看来中间一圈白的是要抠掉的，但是算法认不出来
    #这种可以手动用PS什么的点一个透明像素在里面，再跑一遍算法
    #还有一种情况就是比如一张纸，边缘是黑的，中间是白的，但是这张纸超出了图片的边界，在人看来是不应该抠掉的，但是算法就会把纸中间的白色像素抠掉
    #这种因为抠掉的都是255白，可以用PS手动填充一下，不怎么麻烦
    #这两种边界检测的算法我是想不出来了，目测要用机器学习弄，菜鸡表示......
    img.save( 'done\\' + filename)
 
for root,dir,file in walk("source"):
    for filename in file:
        #抠source文件夹里的所有图片，口完了放在done文件夹里
        cut(root,filename)
