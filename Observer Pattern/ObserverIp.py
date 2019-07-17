""""
观察者模式来验证常用的ip验证
"""

from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """观察者抽象基类"""

    @abstractmethod
    def update(self, observable):
        pass


class Observable:
    """被观察者基类"""

    def __init__(self):
        self.__observers = []

    # 添加观察者
    def add_observer(self, observer):
        self.__observers.append(observer)

    # 移除观察者
    def remove_observer(self, observer):
        self.__observers.remove(observer)

    # 查询当前观察者
    def has_observer(self):
        return self.__observers

    # 状态变更，轮询观察者
    def notify_all_observers(self):
        for observer in self.__observers:
            observer.update(self)


class LoginIp(Observable):
    """本次登录ip"""

    def __init__(self):
        super().__init__()
        self.__ip = ""

    def set_ip(self, ip):
        self.__ip = ip
        self.notify_all_observers()

    @property
    def get_cur_ip(self):
        return self.__ip


def singleton(cls):
    """观察者装饰器，把观察者设为单例模式"""
    d = {}

    def _singleton(*args, **kwargs):
        if cls not in d:
            d[cls] = cls(*args, **kwargs)
        return d[cls]
    return _singleton


@singleton
class LoginIpChecker(Observer):
    """本次登录ip监控"""

    # 常用ip登录列表，如果更为复杂的逻辑，可以记录在该ip登录的次数，最近一次登录的日期。取决于ip数据放在哪中数据结构上
    _ip_list = []

    def update(self, observable):
        if isinstance(observable, LoginIp):
            if self._ip_list and observable.get_cur_ip not in self._ip_list:
                print(f"当前登录ip为{observable.get_cur_ip}和之前登录ip不一致，需要进行验证")
                self._ip_list.append(observable.get_cur_ip)
            elif not self._ip_list:
                print(f"第一次登录，ip为{observable.get_cur_ip}，需要进行验证")
                self._ip_list.append(observable.get_cur_ip)
            else:
                print(f"登录成功")


if __name__ == '__main__':
    # 测试代码
    loginIp = LoginIp()
    loginIpChecker = LoginIpChecker()
    loginIp.add_observer(loginIpChecker)
    print("=======第一次登录========")
    loginIp.set_ip("127.0.0.1")
    print("=======第二次登录========")
    loginIp.set_ip("127.0.0.1")
    print("========第三次异地登录===========")
    loginIp.set_ip("127.99.99.1")
