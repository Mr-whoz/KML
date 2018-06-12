# -*- coding:utf-8 -*-
author = 'Mr-whoz'
date = '2018.4.10'
'''
kml生成包
'''
class ITDKkml:
    def __init__(self,f):
        self.f = f
        self.line_color = 'ffffffff'
        self.line_width = 1
        self.line_hight_start = 0
        self.line_hight_end = 0
        self.point_icon = 'default.png'
        self.point_hight = 0
        self.altitudeMode = ''
        self.point_color = 'ff00ffff'
        self.point_scale = 0.4
    #设置线的样式
    def setting_line(self,line_color= 'ff550077',line_width=1,line_hight_start=0,line_hight_end=0,altitudeMode = ''):
        '''
        @line_color:线的颜色，8位16进制的字符串
        @line_width:线的宽度，默认1
        @line_hight_start:线的起点的高度，默认0
        @line_hight_end:线的终点的高度，默认0
        @aititudeMode:relativeToGround
        '''
        self.line_color = line_color
        self.line_width = line_width
        self.line_hight_start = line_hight_start
        self.line_hight_end = line_hight_end
        if altitudeMode != '':
            self.altitudeMode =  '<altitudeMode>'+altitudeMode+'</altitudeMode>'
    #设置点的样式
    def setting_point(self,point_scale = 0.4,point_color = 'ff00ffff',icon_path = 'default.png',point_hight=0):
        self.point_icon = icon_path
        self.point_hight = point_hight
        self.point_color = point_color
        self.point_scale = point_scale
    #头
    def head(self):
        head = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
<Style id="color_line">
<LineStyle>
<color>'''+self.line_color+'''</color>
<width>'''+str(self.line_width)+'''</width>
</LineStyle>
</Style>
<Style id="icon_style">
<IconStyle><color>'''+self.point_color+'''</color>
<scale>'''+str(self.point_scale)+'''</scale>
<Icon><href>'''+self.point_icon+'''</href></Icon></IconStyle>
</Style>\n'''
        self.f.write(head)
    #尾
    def tail(self):
        tail = '</Document></kml>'
        self.f.write(tail)
    #画点函数
    def draw_point2(self,longitude,latitude):
        point=r'''<Placemark><styleUrl>#icon_style</styleUrl><Point><altitudeMode>relativeToGround</altitudeMode>
			<coordinates>'''+str(longitude)+','+str(latitude)+','+str(self.point_hight)+'''</coordinates></Point></Placemark>'''+'\n'
        self.f.write(point)
    #画边函数
    def draw_edge(self,start,end):
        '''
        @start:一个字典，{'longitude': value,'latitude':value}
        @end: 同上
        '''
        edge=r'''<Placemark><styleUrl>#color_line</styleUrl><LineString>'''+self.altitudeMode+'''<coordinates>'''+str(start['longitude'])+','+str(start['latitude'])+','+str(self.line_hight_start)+' '+\
              str(end['longitude'])+','+str(end['latitude'])+','+str(self.line_hight_end)+\
             '''</coordinates></LineString></Placemark>'''+'\n'
        self.f.write(edge)
    #画原始点
    def draw_orig_point(self,longitude,latitude):
        point=r'''<Placemark><Style><IconStyle><color>'''+self.point_color+'''</color>
<scale>'''+str(self.point_scale)+'''</scale>
<Icon><href>'''+self.point_icon+'''</href></Icon></IconStyle></Style>'''+'''<Point><altitudeMode>relativeToGround</altitudeMode>
<coordinates>'''+str(longitude)+','+str(latitude)+','+str(self.point_hight)+'''</coordinates></Point></Placemark>'''+'\n'
        self.f.write(point)
    #画原始边
    def draw_orig_edge(self,start,end):
        edge=r'''<Placemark><Style><LineStyle>
<color>'''+self.line_color+'''</color>
<width>'''+str(self.line_width)+'''</width>
</LineStyle></Style><LineString>'''+self.altitudeMode+'''<coordinates>'''+str(start['longitude'])+','+str(start['latitude'])+','+str(self.line_hight_start)+' '+\
              str(end['longitude'])+','+str(end['latitude'])+','+str(self.line_hight_end)+\
             '''</coordinates></LineString></Placemark>'''+'\n'
        self.f.write(edge)

    def folder(self,cusor,foder_name):
        head = '<Folder><name>'+str(foder_name)+'</name>'+'\n'
        self.f.write(head)
        for docu in cusor:
            self.draw_point2(longitude=docu['longitude'],latitude=docu['latitude'])
        tail = '</Folder>'+'\n'
        self.f.write(tail)
    #带有description的画点函数
    def draw_point(self,longitude,latitude,Nlist):
        point=r'''<Placemark><description>'''+str(Nlist)+'''</description><Point>
		<coordinates>'''+str(longitude)+','+str(latitude)+','+'''0</coordinates></Point></Placemark>'''+'\n'
        self.f.write(point)
    def egde_folder(self,cusor,foder_name):
        head = '<Folder><name>'+str(foder_name)+'</name>'+'\n'
        self.f.write(head)
        temp_color = '7fff0000'#'64'+str(hex(random.randint(0,16777198))).replace('0x','')
        for docu in cusor:
            self.draw_edge(start=docu['start'],end=docu['end'])
        tail = '</Folder>'+'\n'
        self.f.write(tail)
        pass
    def draw_trace(self,cus):
        trace=''
        for point in cus:
            trace=trace+str(point['longitude'])+','+str(point['latitude'])+',0 '
        content=r'''<Placemark><LineString><coordinates>'''+trace+\
             '''</coordinates></LineString></Placemark>'''+'\n'
        self.f.write(content)
    def draw_edge_describe(self,start,end,describe):
        edge=r'''<Placemark><description>'''+describe+'''</description><LineString>
        <coordinates>'''+str(start['longitude'])+','+str(start['latitude'])+',0 '+\
              str(end['longitude'])+','+str(end['latitude'])+',0'+\
        '''</coordinates></LineString></Placemark>'''+'\n'
        self.f.write(edge)
    def draw_edge_statistic(self,collection):
        self.head()
        for edge in collection.find():
            self.draw_edge(edge['start'],edge['end'])
        self.tail()
    def draw_edge_highAndLow(self,start,end):
        edge=r'''<Placemark><LineString><styleUrl>#color_line</styleUrl><altitudeMode>relativeToGround</altitudeMode><coordinates>'''+str(start['longitude'])+','+str(start['latitude'])+',1.65e+005 '+\
              str(end['longitude'])+','+str(end['latitude'])+',0'+\
             '''</coordinates></LineString></Placemark>'''+'\n'
        self.f.write(edge)
if __name__ == '__main__':
    import pymongo
    file_name = r'links_jp2ip.kmz'
    file_name = file_name.decode('utf-8')
    f=open(file_name,'w')
    paint = ITDKkml(f)
    client = pymongo.MongoClient()
    paint.draw_edge_statistic(collection=client['itdkall_info']['edge'])