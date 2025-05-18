#include "dofbot_kinemarics.h"
#include <kdl_parser/kdl_parser.hpp>
#include <kdl/chainfksolverpos_recursive.hpp>
#include <kdl/chainiksolverpos_lma.hpp>
#include <ros/ros.h>

using namespace KDL;

// 正运动学实现
bool Dofbot::dofbot_getFK(const char *urdf_file, std::vector<double> &joints, std::vector<double> &currentPos) {
    KDL::Tree tree;
    if (!kdl_parser::treeFromFile(urdf_file, tree)) {
        ROS_ERROR("Failed to parse URDF file!");
        return false;
    }

    KDL::Chain chain;
    if (!tree.getChain("base_link", "link5", chain)) {
        ROS_ERROR("Failed to build kinematic chain");
        return false;
    }

    // 检查关节数量是否匹配
    if (joints.size() != chain.getNrOfJoints()) {
        ROS_ERROR("Joint count mismatch. Expected %d, got %zu", chain.getNrOfJoints(), joints.size());
        return false;
    }

    // 转换关节角度到KDL数据结构
    KDL::JntArray jointPositions(chain.getNrOfJoints());
    for (size_t i = 0; i < joints.size(); ++i) {
        jointPositions(i) = joints[i];
    }

    // 计算正运动学
    KDL::ChainFkSolverPos_recursive fk_solver(chain);
    KDL::Frame end_effector_pose;
    if (fk_solver.JntToCart(jointPositions, end_effector_pose) < 0) {
        ROS_ERROR("FK solver failed!");
        return false;
    }

    // 提取位置和姿态
    currentPos.clear();
    currentPos.push_back(end_effector_pose.p.x());
    currentPos.push_back(end_effector_pose.p.y());
    currentPos.push_back(end_effector_pose.p.z());

    double roll, pitch, yaw;
    end_effector_pose.M.GetRPY(roll, pitch, yaw);
    currentPos.push_back(roll);
    currentPos.push_back(pitch);
    currentPos.push_back(yaw);

    return true;
}

// 逆运动学实现
bool Dofbot::dofbot_getIK(const char *urdf_file, std::vector<double> &targetXYZ, std::vector<double> &targetRPY, std::vector<double> &outjoints) {
    KDL::Tree tree;
    if (!kdl_parser::treeFromFile(urdf_file, tree)) {
        ROS_ERROR("Failed to parse URDF file!");
        return false;
    }

    KDL::Chain chain;
    if (!tree.getChain("base_link", "link5", chain)) {
        ROS_ERROR("Failed to build kinematic chain");
        return false;
    }

    // 创建逆运动学求解器
    KDL::ChainIkSolverPos_LMA ik_solver(chain);

    // 构建目标位姿
    KDL::Frame target_frame;
    target_frame.p = KDL::Vector(targetXYZ[0], targetXYZ[1], targetXYZ[2]);
    target_frame.M = KDL::Rotation::RPY(targetRPY[0], targetRPY[1], targetRPY[2]);

    // 初始关节角猜测（设为当前关节角或零）
    KDL::JntArray joint_seed(chain.getNrOfJoints());
    for (size_t i = 0; i < joint_seed.rows(); ++i) {
        joint_seed(i) = 0.0; // 默认初始猜测
    }

    // 计算逆解
    KDL::JntArray result_joints(chain.getNrOfJoints());
    int ik_result = ik_solver.CartToJnt(joint_seed, target_frame, result_joints);

    if (ik_result < 0) {
        ROS_ERROR("IK solver failed with code: %d", ik_result);
        return false;
    }

    // 输出关节角
    outjoints.clear();
    for (size_t i = 0; i < result_joints.rows(); ++i) {
        outjoints.push_back(result_joints(i));
    }

    return true;
}