# Tester Agent Strategies Reference

## Overview
This document provides a comprehensive reference for all tester agent strategies in the Universal Tester-Agent (UTA) system. Each strategy implements a specific testing approach to validate different aspects of AI agent behavior.

## Strategy Interface
All strategies inherit from `BaseStrategy` and implement three core methods:
- `first_message(scenario)`: Generate the initial user message
- `next_message(last_agent_response, scenario)`: Generate follow-up messages based on agent responses
- `should_continue(conversation, scenario)`: Determine if the conversation should continue

---

## ✅ IMPLEMENTED & ACTIVE STRATEGIES

### 1. FlowIntent Strategy
**File**: `agents/strategies/flow_intent.py`  
**Status**: ✅ Active (Registered)  
**Purpose**: Basic conversational flow testing with clarification and confirmation

**Intent**:
- Test fundamental conversational capabilities
- Validate intent recognition and clarification handling
- Ensure proper confirmation and input flows

**Behavior**:
- Sends initial message from scenario
- Provides clarification if agent asks ("can you clarify", "what do you mean")
- Confirms proposed actions when `outcome == "pending_confirmation"`
- Provides input when agent requests ("please provide", "i need", "enter")
- Stops when max turns reached or goal achieved

**Use Cases**:
- Core scenarios requiring basic flow validation
- Intent recognition testing
- Clarification and confirmation flows
- Input provision testing

**Example Scenarios**:
- `CORE_001_INTENT_SUCCESS`: Basic intent recognition
- `CORE_002_AMBIGUOUS_CLARIFICATION`: Clarification handling
- `COL_S01_PROMISE_TO_PAY`: Payment confirmation flow

---

### 2. ToolHappyPath Strategy
**File**: `agents/strategies/tool_happy_path.py`  
**Status**: ✅ Active (Registered)  
**Purpose**: Tests successful tool usage and execution

**Intent**:
- Validate tool identification and execution capabilities
- Test input provision for tool execution
- Ensure proper tool result handling and confirmation

**Behavior**:
- Sends tool request message from scenario
- Provides necessary input when agent asks ("please provide", "i need", "enter")
- Confirms tool execution when requested ("confirm", "proceed", "continue")
- Acknowledges successful tool completion
- Stops when tool is successfully executed or max turns reached

**Use Cases**:
- Core scenarios requiring tool execution
- Tool integration testing
- Success path validation
- Tool input and confirmation flows

**Example Scenarios**:
- `CORE_003_TOOL_HAPPY_PATH`: Tool execution success path

---

## 🔄 IMPLEMENTED BUT NOT REGISTERED

### 3. MemoryCarry Strategy
**File**: `agents/strategies/memory_carry.py`  
**Status**: 🔄 Ready (Not Registered)  
**Purpose**: Tests memory and context carry across conversation turns

**Intent**:
- Validate conversational memory and context retention
- Test entity carry and slot filling capabilities
- Ensure proper context awareness across turns

**Behavior**:
- Sends initial message with context information
- References earlier information in follow-up messages
- Tests if agent maintains context and memory
- Provides context-specific follow-up questions
- Stops after memory test is complete (3+ turns)

**Use Cases**:
- Testing conversational memory
- Context awareness validation
- Entity carry testing
- Slot filling validation

**Example Use Cases**:
- "Thanks for helping with my checking account. Can you also check the balance?"
- "About that $100 payment we discussed, when will it be processed?"
- "By the way, my name is John Doe. Can you update my profile?"

---

## ❌ PLANNED STRATEGIES (Not Yet Implemented)

### 4. ToolError Strategy
**File**: `agents/strategies/tool_error.py`  
**Status**: ❌ Planned (Empty File)  
**Purpose**: Tests error handling and recovery in tool execution

**Intent**:
- Validate tool failure handling capabilities
- Test error recovery and fallback behavior
- Ensure proper error messaging and user guidance

**Planned Behavior**:
- Sends tool requests that will fail
- Tests error handling and recovery flows
- Validates fallback mechanisms
- Ensures proper error messaging

**Use Cases**:
- Tool failure scenarios
- Error recovery testing
- Resilience validation
- Fallback behavior testing

---

### 5. Disturbance Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests agent behavior under various disturbances and edge cases

**Intent**:
- Validate robustness under noisy conditions
- Test interruption recovery capabilities
- Ensure proper handling of edge cases and unexpected inputs

**Planned Behavior**:
- Introduces various disturbances (noise, interruptions, edge cases)
- Tests agent's ability to handle unexpected situations
- Validates recovery from disturbances
- Ensures consistent behavior under stress

**Use Cases**:
- Noise handling testing
- Interruption recovery
- Edge case validation
- Robustness testing

---

### 6. Planner Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests multi-step planning and complex task execution

**Intent**:
- Validate task decomposition capabilities
- Test step-by-step execution and planning
- Ensure proper handling of complex, multi-step workflows

**Planned Behavior**:
- Sends complex, multi-step task requests
- Tests task decomposition and planning
- Validates step-by-step execution
- Ensures proper workflow management

**Use Cases**:
- Complex workflow testing
- Multi-step task validation
- Planning capability testing
- Task decomposition validation

---

### 7. Persona Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests agent behavior with different user personas and contexts

**Intent**:
- Validate persona adaptation capabilities
- Test context-aware responses
- Ensure proper user profiling and personalization

**Planned Behavior**:
- Adopts different user personas (age, background, expertise level)
- Tests persona-specific responses
- Validates context awareness
- Ensures proper personalization

**Use Cases**:
- User adaptation testing
- Personalization validation
- Context awareness testing
- Persona-specific behavior validation

---

### 8. PIIProbe Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests privacy and PII handling capabilities

**Intent**:
- Validate PII detection and protection
- Test privacy compliance and data handling
- Ensure proper data protection and privacy safeguards

**Planned Behavior**:
- Introduces PII in conversations
- Tests PII detection and protection
- Validates privacy compliance
- Ensures proper data handling

**Use Cases**:
- Privacy compliance testing
- PII protection validation
- Data handling testing
- Privacy safeguard validation

---

### 9. Interruption Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests agent behavior when conversations are interrupted

**Intent**:
- Validate interruption handling capabilities
- Test conversation recovery and state management
- Ensure proper handling of conversation disruptions

**Planned Behavior**:
- Introduces conversation interruptions
- Tests interruption recovery
- Validates state management
- Ensures proper conversation resumption

**Use Cases**:
- Conversation resilience testing
- Interruption recovery validation
- State management testing
- Conversation continuity validation

---

### 10. RepeatProbe Strategy
**File**: Not yet created  
**Status**: ❌ Planned  
**Purpose**: Tests agent behavior with repeated or similar requests

**Intent**:
- Validate consistency in responses
- Test learning from repetition
- Ensure proper handling of repeated requests

**Planned Behavior**:
- Sends repeated or similar requests
- Tests response consistency
- Validates learning from repetition
- Ensures proper handling of repeated patterns

**Use Cases**:
- Consistency testing
- Repetition handling validation
- Learning capability testing
- Pattern recognition validation

---

## Strategy Selection Guidelines

### When to Use Each Strategy

**FlowIntent**: Use for basic conversational flows, intent recognition, and simple clarification scenarios.

**ToolHappyPath**: Use when testing tool execution, integration, and success paths.

**MemoryCarry**: Use when testing conversational memory, context retention, and entity carry.

**ToolError**: Use when testing error handling, resilience, and fallback behavior.

**Disturbance**: Use when testing robustness, edge cases, and noise handling.

**Planner**: Use when testing complex workflows, multi-step tasks, and planning capabilities.

**Persona**: Use when testing user adaptation, personalization, and context awareness.

**PIIProbe**: Use when testing privacy compliance, data protection, and PII handling.

**Interruption**: Use when testing conversation resilience, state management, and interruption recovery.

**RepeatProbe**: Use when testing consistency, repetition handling, and learning capabilities.

---

## Implementation Status Summary

| Strategy | Status | Implementation | Registration | Priority |
|----------|--------|----------------|--------------|----------|
| **FlowIntent** | ✅ Active | Complete | ✅ Registered | High |
| **ToolHappyPath** | ✅ Active | Complete | ✅ Registered | High |
| **MemoryCarry** | 🔄 Ready | Complete | ❌ Not registered | Medium |
| **ToolError** | ❌ Planned | Empty file | ❌ Not registered | Medium |
| **Disturbance** | ❌ Planned | Not implemented | ❌ Not registered | Low |
| **Planner** | ❌ Planned | Not implemented | ❌ Not registered | Medium |
| **Persona** | ❌ Planned | Not implemented | ❌ Not registered | Low |
| **PIIProbe** | ❌ Planned | Not implemented | ❌ Not registered | High |
| **Interruption** | ❌ Planned | Not implemented | ❌ Not registered | Low |
| **RepeatProbe** | ❌ Planned | Not implemented | ❌ Not registered | Low |

---

## Next Steps

1. **Immediate**: Register `MemoryCarryStrategy` to make it available
2. **Short-term**: Implement `ToolErrorStrategy` for error handling testing
3. **Medium-term**: Implement `PIIProbeStrategy` for privacy compliance testing
4. **Long-term**: Implement remaining strategies for comprehensive testing coverage

---

*Last Updated: [Current Date]*  
*Version: 0.1*
