#!/usr/bin/env python

import rospy
import rospkg
import tornado.ioloop
import tornado.web

rospack = rospkg.RosPack()
packages = sorted(rospack.list())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Available ROS Packages:</h1>")
        self.write("<ul>")
        for package in packages:
            self.write("<li><a href='/"+package+"/'>"+package+"</a></li>")
        self.write("</l>")

class CrossOriginStaticFileHandler(tornado.web.StaticFileHandler):
    def get(self, config):
        self.set_header("Access-Control-Allow-Origin", "*")
        return super(CrossOriginStaticFileHandler, self).get(config)

def main():
    rospy.init_node('ros_package_web_server', anonymous=True)
    port = default_param = rospy.get_param('~port', 8888)

    handlers = [
        ("/", MainHandler),
    ]
    for package in packages:
        handlers.append((r'/'+package+'/(.*)', CrossOriginStaticFileHandler, {'path': rospack.get_path(package)}))


    def log_request(handler):
        if handler.get_status() < 400:
            log_method = rospy.loginfo
        elif handler.get_status() < 500:
            log_method = rospy.logwarn
        else:
            log_method = rospy.logerror
        log_method("%d %s", handler.get_status(), handler._request_summary())

    application = tornado.web.Application(handlers, debug = True, log_function = log_request)

    application.listen(port)

    def shutdown_hook():
        tornado.ioloop.IOLoop.instance().stop()
    rospy.on_shutdown(shutdown_hook)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
