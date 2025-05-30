// Generated by gencpp from file yahboomcar_msgs/Position.msg
// DO NOT EDIT!


#ifndef YAHBOOMCAR_MSGS_MESSAGE_POSITION_H
#define YAHBOOMCAR_MSGS_MESSAGE_POSITION_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace yahboomcar_msgs
{
template <class ContainerAllocator>
struct Position_
{
  typedef Position_<ContainerAllocator> Type;

  Position_()
    : angleX(0.0)
    , angleY(0.0)
    , distance(0.0)  {
    }
  Position_(const ContainerAllocator& _alloc)
    : angleX(0.0)
    , angleY(0.0)
    , distance(0.0)  {
  (void)_alloc;
    }



   typedef float _angleX_type;
  _angleX_type angleX;

   typedef float _angleY_type;
  _angleY_type angleY;

   typedef float _distance_type;
  _distance_type distance;





  typedef boost::shared_ptr< ::yahboomcar_msgs::Position_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::yahboomcar_msgs::Position_<ContainerAllocator> const> ConstPtr;

}; // struct Position_

typedef ::yahboomcar_msgs::Position_<std::allocator<void> > Position;

typedef boost::shared_ptr< ::yahboomcar_msgs::Position > PositionPtr;
typedef boost::shared_ptr< ::yahboomcar_msgs::Position const> PositionConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::yahboomcar_msgs::Position_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::yahboomcar_msgs::Position_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::yahboomcar_msgs::Position_<ContainerAllocator1> & lhs, const ::yahboomcar_msgs::Position_<ContainerAllocator2> & rhs)
{
  return lhs.angleX == rhs.angleX &&
    lhs.angleY == rhs.angleY &&
    lhs.distance == rhs.distance;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::yahboomcar_msgs::Position_<ContainerAllocator1> & lhs, const ::yahboomcar_msgs::Position_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace yahboomcar_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::yahboomcar_msgs::Position_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::yahboomcar_msgs::Position_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::yahboomcar_msgs::Position_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::yahboomcar_msgs::Position_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::yahboomcar_msgs::Position_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::yahboomcar_msgs::Position_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::yahboomcar_msgs::Position_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e4df5e09e92d9d2b4758c9aab7a9ebeb";
  }

  static const char* value(const ::yahboomcar_msgs::Position_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe4df5e09e92d9d2bULL;
  static const uint64_t static_value2 = 0x4758c9aab7a9ebebULL;
};

template<class ContainerAllocator>
struct DataType< ::yahboomcar_msgs::Position_<ContainerAllocator> >
{
  static const char* value()
  {
    return "yahboomcar_msgs/Position";
  }

  static const char* value(const ::yahboomcar_msgs::Position_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::yahboomcar_msgs::Position_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 angleX\n"
"float32 angleY\n"
"float32 distance\n"
;
  }

  static const char* value(const ::yahboomcar_msgs::Position_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::yahboomcar_msgs::Position_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.angleX);
      stream.next(m.angleY);
      stream.next(m.distance);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Position_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::yahboomcar_msgs::Position_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::yahboomcar_msgs::Position_<ContainerAllocator>& v)
  {
    s << indent << "angleX: ";
    Printer<float>::stream(s, indent + "  ", v.angleX);
    s << indent << "angleY: ";
    Printer<float>::stream(s, indent + "  ", v.angleY);
    s << indent << "distance: ";
    Printer<float>::stream(s, indent + "  ", v.distance);
  }
};

} // namespace message_operations
} // namespace ros

#endif // YAHBOOMCAR_MSGS_MESSAGE_POSITION_H
