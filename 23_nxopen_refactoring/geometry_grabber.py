import NXOpen
import NXOpen.UF
import os
import threading
import multiprocessing
import time as tt


APPDATA = os.environ['APPDATA']


class GeometryGrabber:
    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.session_uf = NXOpen.UF.UFSession.GetUFSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.bodies = []
        self.file_cache = ''

    def write_file_cache(self, body, values):
        with multiprocessing.Lock():
            with open(self.file_cache, 'a') as cached_geometry:
                cached_geometry.write('--\n{0}-{1}\n'.format(body, values))

    def set_file_cache(self, file_name=''):
        try:
            if not file_name:
                folder_name = os.path.join(APPDATA, 'teamcenter', 'NX_DMCache')
                file_name = os.path.join(folder_name, 'cached_geometry.txt')
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                if not os.path.isfile(file_name):
                    with open(file_name, 'w') as cache:
                        cache.write()
            self.file_cache = file_name
        except Exception as ex:
            raise ex

    def get_file_cache(self):
        return self.file_cache

    def grab_geometry(self, bodies, vertices=[], points=[]):
        with multiprocessing.Lock():
            for body in bodies:
                vertices = []
                points = []
                for edge in body.GetEdges():
                    [vertices.append(vert) for vert in edge.GetVertices()]
                for point in vertices:
                    points.append((point.X, point.Y, point.Z))

    def get_object_chunks(self, thread_num, out=[], last=0.0):
        obj_in_chunk = len(self.bodies) / float(thread_num)
        while last < len(self.bodies):
            out.append(self.bodies[int(last):int(last + obj_in_chunk)])
            last += obj_in_chunk
        return out

    def process_objects(self, bodies=[], temp_body_tag=0):
        while True:
            temp_body_tag = self.session_uf.Obj.CycleObjsInPart(
                self.work_part.Tag,
                NXOpen.UF.UFConstants.UF_solid_type,
                temp_body_tag)
            if temp_body_tag == 0:
                break
            else:
                theType, the_subtype = self.session_uf.Obj.AskTypeAndSubtype(
                    temp_body_tag)
                if the_subtype == NXOpen.UF.UFConstants.UF_solid_body_subtype:
                    bodies.append(
                        NXOpen.TaggedObjectManager.GetTaggedObject(
                            temp_body_tag))
        self.bodies = bodies


def start_multithread_execution(app, chunks):
    vts = []
    pts = []
    threadList = []
    time1 = tt.time()
    for index in range(thread_num):
        set_ = chunks[index]
        vts.insert(index, [])
        pts.insert(index, [])
        threadList.insert(index, threading.Thread(
            target=app.grab_geometry, args=(set_, vts[index], pts[index])))
        threadList[index].start()
    for thread in threadList:
        thread.join()
    time2 = tt.time() - time1


def start_single_thread_execution(app):
    v1, p1 = [], []
    t1 = threading.Thread(target=app.grab_geometry, args=(app.bodies, v1, p1))
    t1.start()
    t1.join()


def show_report_info(app):
    app.lw.WriteLine(str(len(app.bodies)))
    app.lw.WriteLine(str(time2))
    app.lw.WriteLine('Completed')


def main(thread_num=4):
    app = GeometryGrabber()
    app.lw.Open()
    app.process_objects()
    app.set_file_cache()
    chunks = app.get_object_chunks(thread_num)
    time1 = tt.time()
    if len(app.bodies) > 1:
        start_multithread_execution(app, chunks)
    elif len(app.bodies) == 1:
        start_single_thread_execution(app)
    else:
        pass
    time2 = tt.time() - time2
    show_report_info(app)


if __name__ == '__main__':
    main()
