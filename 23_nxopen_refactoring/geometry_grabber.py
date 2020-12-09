import NXOpen
import NXOpen.UF
import os
import threading
import multiprocessing
import time as tt


class GeometryGrabber:
    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.session_uf = NXOpen.UF.UFSession.GetUFSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.bodies = []
        self.file_cache = []

    def write_cache_file(self, body, values):
        with multiprocessing.Lock():
            with open(self.file_cache, 'a') as cached_geometry:
                cached_geometry.write('--\n{0}-{1}\n'.format(body, values))

    def get_cache_file(self):
        try:
            folder_name = '%s\\teamcenter\\NX_DMCache' % os.environ['APPDATA']
            file_name = '%s\\teamcenter\\NX_DMCache\\cached_geometry.txt' % os.environ[
                'APPDATA']
            if os.path.isdir(folder_name):
                pass
            else:
                os.mkdir(folder_name)
            if os.path.isfile(file_name):
                self.file_cache = file_name
                # return file_name
            else:
                with open(file_name, 'a') as cache:
                    cache.close()
                self.file_cache = file_name
                # return file_name
        except Exception as ex:
            #self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'get_cache_file failed with %s' %ex)
            raise ex
        pass

    def grab_geometry(self, bodies, vertices=[], points=[]):
        with multiprocessing.Lock():
            for body in bodies:
                edges = []
                [edges.append(edge) for edge in body.GetEdges()]
                vertices = []
                for edge in edges:
                    [vertices.append(vert) for vert in edge.GetVertices()]
                points = []
                for point in vertices:
                    points.append((point.X, point.Y, point.Z))
                # self.write_cache_file(body,points)

    def chunkIt(self, thread_num, out=[], last=0.0):
        avg = len(self.bodies) / float(thread_num)
        while last < len(self.bodies):
            out.append(self.bodies[int(last):int(last + avg)])
            last += avg
        return out

    def process_objects(self, bodies=[], tmpBodyTag=0):
        while True:
            tmpBodyTag = self.session_uf.Obj.CycleObjsInPart(
                self.work_part.Tag, NXOpen.UF.UFConstants.UF_solid_type, tmpBodyTag)
            if tmpBodyTag == 0:
                break
            else:
                theType, theSubType = self.session_uf.Obj.AskTypeAndSubtype(
                    tmpBodyTag)
                if theSubType == NXOpen.UF.UFConstants.UF_solid_body_subtype:
                    bodies.append(
                        NXOpen.TaggedObjectManager.GetTaggedObject(tmpBodyTag))
        self.bodies = bodies
        # return bodies


def main(thread_num=4):
    app = GeometryGrabber()
    app.lw.Open()
    app.process_objects()
    app.get_cache_file()
    chunks = app.chunkIt(thread_num)
    # multithreading section
    if len(app.bodies) > 1:
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
    # single thread section
    elif len(app.bodies) == 1:
        time1 = tt.time()
        v1, p1 = [], []
        t1 = threading.Thread(target=app.grab_geometry,
                              args=(app.bodies, v1, p1))
        t1.start()
        t1.join()
        time2 = tt.time() - time2
    else:
        pass
    # report section
    app.lw.WriteLine(str(len(app.bodies)))
    app.lw.WriteLine(str(time2))
    app.lw.WriteLine('Completed')
    return None


if __name__ == '__main__':
    main()
