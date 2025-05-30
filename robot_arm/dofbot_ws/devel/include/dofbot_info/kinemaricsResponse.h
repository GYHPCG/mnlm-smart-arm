// Generated by gencpp from file dofbot_info/kinemaricsResponse.msg
// DO NOT EDIT!


#ifndef DOFBOT_INFO_MESSAGE_KINEMARICSRESPONSE_H
#define DOFBOT_INFO_MESSAGE_KINEMARICSRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace dofbot_info
{
template <class ContainerAllocator>
struct kinemaricsResponse_
{
  typedef kinemaricsResponse_<ContainerAllocator> Type;

  kinemaricsResponse_()
    : joint1(0.0)
    , joint2(0.0)
    , joint3(0.0)
    , joint4(0.0)
    , joint5(0.0)
    , joint6(0.0)
    , x(0.0)
    , y(0.0)
    , z(0.0)
    , Roll(0.0)
    , Pitch(0.0)
    , Yaw(0.0)  {
    }
  kinemaricsResponse_(const ContainerAllocator& _alloc)
    : joint1(0.0)
    , joint2(0.0)
    , joint3(0.0)
    , joint4(0.0)
    , joint5(0.0)
    , joint6(0.0)
    , x(0.0)
    , y(0.0)
    , z(0.0)
    , Roll(0.0)
    , Pitch(0.0)
    , Yaw(0.0)  {
  (void)_alloc;
    }



   typedef double _joint1_type;
  _joint1_type joint1;

   typedef double _joint2_type;
  _joint2_type joint2;

   typedef double _joint3_type;
  _joint3_type joint3;

   typedef double _joint4_type;
  _joint4_type joint4;

   typedef double _joint5_type;
  _joint5_type joint5;

   typedef double _joint6_type;
  _joint6_type joint6;

   typedef double _x_type;
  _x_type x;

   typedef double _y_type;
  _y_type y;

   typedef double _z_type;
  _z_type z;

   typedef double _Roll_type;
  _Roll_type Roll;

   typedef double _Pitch_type;
  _Pitch_type Pitch;

   typedef double _Yaw_type;
  _Yaw_type Yaw;





  typedef boost::shared_ptr< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> const> ConstPtr;

}; // struct kinemaricsResponse_

typedef ::dofbot_info::kinemaricsResponse_<std::allocator<void> > kinemaricsResponse;

typedef boost::shared_ptr< ::dofbot_info::kinemaricsResponse > kinemaricsResponsePtr;
typedef boost::shared_ptr< ::dofbot_info::kinemaricsResponse const> kinemaricsResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dofbot_info::kinemaricsResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::dofbot_info::kinemaricsResponse_<ContainerAllocator1> & lhs, const ::dofbot_info::kinemaricsResponse_<ContainerAllocator2> & rhs)
{
  return lhs.joint1 == rhs.joint1 &&
    lhs.joint2 == rhs.joint2 &&
    lhs.joint3 == rhs.joint3 &&
    lhs.joint4 == rhs.joint4 &&
    lhs.joint5 == rhs.joint5 &&
    lhs.joint6 == rhs.joint6 &&
    lhs.x == rhs.x &&
    lhs.y == rhs.y &&
    lhs.z == rhs.z &&
    lhs.Roll == rhs.Roll &&
    lhs.Pitch == rhs.Pitch &&
    lhs.Yaw == rhs.Yaw;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::dofbot_info::kinemaricsResponse_<ContainerAllocator1> & lhs, const ::dofbot_info::kinemaricsResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace dofbot_info

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "906df963bc5a51f2145b13de1507f439";
  }

  static const char* value(const ::dofbot_info::kinemaricsResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x906df963bc5a51f2ULL;
  static const uint64_t static_value2 = 0x145b13de1507f439ULL;
};

template<class ContainerAllocator>
struct DataType< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dofbot_info/kinemaricsResponse";
  }

  static const char* value(const ::dofbot_info::kinemaricsResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# response\n"
"float64 joint1\n"
"float64 joint2\n"
"float64 joint3\n"
"float64 joint4\n"
"float64 joint5\n"
"float64 joint6\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 Roll\n"
"float64 Pitch\n"
"float64 Yaw\n"
"\n"
"\n"
"\n"
;
  }

  static const char* value(const ::dofbot_info::kinemaricsResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.joint1);
      stream.next(m.joint2);
      stream.next(m.joint3);
      stream.next(m.joint4);
      stream.next(m.joint5);
      stream.next(m.joint6);
      stream.next(m.x);
      stream.next(m.y);
      stream.next(m.z);
      stream.next(m.Roll);
      stream.next(m.Pitch);
      stream.next(m.Yaw);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct kinemaricsResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dofbot_info::kinemaricsResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dofbot_info::kinemaricsResponse_<ContainerAllocator>& v)
  {
    s << indent << "joint1: ";
    Printer<double>::stream(s, indent + "  ", v.joint1);
    s << indent << "joint2: ";
    Printer<double>::stream(s, indent + "  ", v.joint2);
    s << indent << "joint3: ";
    Printer<double>::stream(s, indent + "  ", v.joint3);
    s << indent << "joint4: ";
    Printer<double>::stream(s, indent + "  ", v.joint4);
    s << indent << "joint5: ";
    Printer<double>::stream(s, indent + "  ", v.joint5);
    s << indent << "joint6: ";
    Printer<double>::stream(s, indent + "  ", v.joint6);
    s << indent << "x: ";
    Printer<double>::stream(s, indent + "  ", v.x);
    s << indent << "y: ";
    Printer<double>::stream(s, indent + "  ", v.y);
    s << indent << "z: ";
    Printer<double>::stream(s, indent + "  ", v.z);
    s << indent << "Roll: ";
    Printer<double>::stream(s, indent + "  ", v.Roll);
    s << indent << "Pitch: ";
    Printer<double>::stream(s, indent + "  ", v.Pitch);
    s << indent << "Yaw: ";
    Printer<double>::stream(s, indent + "  ", v.Yaw);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DOFBOT_INFO_MESSAGE_KINEMARICSRESPONSE_H
