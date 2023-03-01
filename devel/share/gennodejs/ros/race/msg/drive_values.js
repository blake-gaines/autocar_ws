// Auto-generated. Do not edit!

// (in-package race.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class drive_values {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pid_vel = null;
      this.pid_error = null;
      this.z = null;
      this.a = null;
      this.b = null;
      this.dist_CD = null;
      this.dist_AB = null;
      this.alpha = null;
      this.realvel = null;
      this.theta1 = null;
      this.theta2 = null;
    }
    else {
      if (initObj.hasOwnProperty('pid_vel')) {
        this.pid_vel = initObj.pid_vel
      }
      else {
        this.pid_vel = 0.0;
      }
      if (initObj.hasOwnProperty('pid_error')) {
        this.pid_error = initObj.pid_error
      }
      else {
        this.pid_error = 0.0;
      }
      if (initObj.hasOwnProperty('z')) {
        this.z = initObj.z
      }
      else {
        this.z = 0.0;
      }
      if (initObj.hasOwnProperty('a')) {
        this.a = initObj.a
      }
      else {
        this.a = 0.0;
      }
      if (initObj.hasOwnProperty('b')) {
        this.b = initObj.b
      }
      else {
        this.b = 0.0;
      }
      if (initObj.hasOwnProperty('dist_CD')) {
        this.dist_CD = initObj.dist_CD
      }
      else {
        this.dist_CD = 0.0;
      }
      if (initObj.hasOwnProperty('dist_AB')) {
        this.dist_AB = initObj.dist_AB
      }
      else {
        this.dist_AB = 0.0;
      }
      if (initObj.hasOwnProperty('alpha')) {
        this.alpha = initObj.alpha
      }
      else {
        this.alpha = 0.0;
      }
      if (initObj.hasOwnProperty('realvel')) {
        this.realvel = initObj.realvel
      }
      else {
        this.realvel = 0.0;
      }
      if (initObj.hasOwnProperty('theta1')) {
        this.theta1 = initObj.theta1
      }
      else {
        this.theta1 = 0.0;
      }
      if (initObj.hasOwnProperty('theta2')) {
        this.theta2 = initObj.theta2
      }
      else {
        this.theta2 = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type drive_values
    // Serialize message field [pid_vel]
    bufferOffset = _serializer.float32(obj.pid_vel, buffer, bufferOffset);
    // Serialize message field [pid_error]
    bufferOffset = _serializer.float32(obj.pid_error, buffer, bufferOffset);
    // Serialize message field [z]
    bufferOffset = _serializer.float32(obj.z, buffer, bufferOffset);
    // Serialize message field [a]
    bufferOffset = _serializer.float32(obj.a, buffer, bufferOffset);
    // Serialize message field [b]
    bufferOffset = _serializer.float32(obj.b, buffer, bufferOffset);
    // Serialize message field [dist_CD]
    bufferOffset = _serializer.float32(obj.dist_CD, buffer, bufferOffset);
    // Serialize message field [dist_AB]
    bufferOffset = _serializer.float32(obj.dist_AB, buffer, bufferOffset);
    // Serialize message field [alpha]
    bufferOffset = _serializer.float32(obj.alpha, buffer, bufferOffset);
    // Serialize message field [realvel]
    bufferOffset = _serializer.float32(obj.realvel, buffer, bufferOffset);
    // Serialize message field [theta1]
    bufferOffset = _serializer.float32(obj.theta1, buffer, bufferOffset);
    // Serialize message field [theta2]
    bufferOffset = _serializer.float32(obj.theta2, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type drive_values
    let len;
    let data = new drive_values(null);
    // Deserialize message field [pid_vel]
    data.pid_vel = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [pid_error]
    data.pid_error = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [z]
    data.z = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [a]
    data.a = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [b]
    data.b = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dist_CD]
    data.dist_CD = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dist_AB]
    data.dist_AB = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [alpha]
    data.alpha = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [realvel]
    data.realvel = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [theta1]
    data.theta1 = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [theta2]
    data.theta2 = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 44;
  }

  static datatype() {
    // Returns string type for a message object
    return 'race/drive_values';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b3201a025913db3e51dc81dc52587e75';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 pid_vel
    float32 pid_error
    float32 z
    float32 a
    float32 b
    float32 dist_CD
    float32 dist_AB
    float32 alpha
    float32 realvel
    float32 theta1
    float32 theta2
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new drive_values(null);
    if (msg.pid_vel !== undefined) {
      resolved.pid_vel = msg.pid_vel;
    }
    else {
      resolved.pid_vel = 0.0
    }

    if (msg.pid_error !== undefined) {
      resolved.pid_error = msg.pid_error;
    }
    else {
      resolved.pid_error = 0.0
    }

    if (msg.z !== undefined) {
      resolved.z = msg.z;
    }
    else {
      resolved.z = 0.0
    }

    if (msg.a !== undefined) {
      resolved.a = msg.a;
    }
    else {
      resolved.a = 0.0
    }

    if (msg.b !== undefined) {
      resolved.b = msg.b;
    }
    else {
      resolved.b = 0.0
    }

    if (msg.dist_CD !== undefined) {
      resolved.dist_CD = msg.dist_CD;
    }
    else {
      resolved.dist_CD = 0.0
    }

    if (msg.dist_AB !== undefined) {
      resolved.dist_AB = msg.dist_AB;
    }
    else {
      resolved.dist_AB = 0.0
    }

    if (msg.alpha !== undefined) {
      resolved.alpha = msg.alpha;
    }
    else {
      resolved.alpha = 0.0
    }

    if (msg.realvel !== undefined) {
      resolved.realvel = msg.realvel;
    }
    else {
      resolved.realvel = 0.0
    }

    if (msg.theta1 !== undefined) {
      resolved.theta1 = msg.theta1;
    }
    else {
      resolved.theta1 = 0.0
    }

    if (msg.theta2 !== undefined) {
      resolved.theta2 = msg.theta2;
    }
    else {
      resolved.theta2 = 0.0
    }

    return resolved;
    }
};

module.exports = drive_values;
